import logging
import operator
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.model_manager import ModelManager
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    tenant_id: str
    contact_id: str
    channel: str
    context: dict[str, Any]


@tool
def search_properties(
    min_price: int | None = None,
    max_price: int | None = None,
    bedrooms: int | None = None,
    property_type: str | None = None,
) -> str:
    """Busca imóveis disponíveis no portfólio da imobiliária. Use quando o lead perguntar sobre imóveis disponíveis."""
    return (
        f"Buscando imóveis: preço={min_price}-{max_price}, quartos={bedrooms}, tipo={property_type}"
    )


@tool
def schedule_visit(
    client_name: str,
    preferred_date: str,
    preferred_time: str,
    property_address: str,
) -> str:
    """Agenda uma visita a um imóvel. Use quando o lead quiser agendar uma visita."""
    return f"Visita agendada: {client_name} em {preferred_date} às {preferred_time} no endereço {property_address}"


@tool
def send_contact_info(
    name: str,
    phone: str | None = None,
    email: str | None = None,
    message: str | None = None,
) -> str:
    """Encaminha o contato para um corretor humano. Use quando o lead pedir para falar com uma pessoa ou quando a negociação exigir atenção humana."""
    return f"Contato encaminhado: {name}, tel={phone}, email={email}, msg={message}"


@tool
def get_property_details(property_id: str) -> str:
    """Obtém detalhes completos de um imóvel específico. Use quando o lead pedir mais informações sobre um imóvel."""
    return f"Detalhes do imóvel {property_id}: informações carregadas"


@tool
def create_follow_up(
    client_name: str,
    follow_up_date: str,
    message: str,
) -> str:
    """Cria um follow-up automático para o lead. Use quando precisar retomar contato com o lead em data futura."""
    return f"Follow-up criado: {client_name} em {follow_up_date} com mensagem: {message}"


tools = [
    search_properties,
    schedule_visit,
    send_contact_info,
    get_property_details,
    create_follow_up,
]


class ImobProAgent:
    def __init__(
        self,
        tenant_name: str,
        agent_name: str,
        commercial_rules: str = "",
        llm_model: str = "gpt-4o",
    ):
        self.tenant_name = tenant_name
        self.agent_name = agent_name
        self.commercial_rules = commercial_rules
        self.llm_model = llm_model
        self.tools = tools
        self._model_manager = ModelManager()

    async def _setup_llm(self) -> None:
        """Configura o LLM com o provider correto, carregando o modelo se necessário."""
        provider = self._model_manager.get_provider_for_model(self.llm_model)

        if provider is None:
            # Modelo não está carregado — tentar carregar
            result = await self._model_manager.ensure_loaded(
                self.llm_model,
                fallback_model=settings.MODEL_DEFAULT,
            )
            if result.get("status") == "error":
                raise RuntimeError(f"Não foi possível carregar o modelo {self.llm_model}: {result.get('error')}")
            provider = self._model_manager.get_provider_for_model(self.llm_model)
            # Usar o modelo que foi efetivamente carregado
            if result.get("model") and result["model"] != self.llm_model:
                self.llm_model = result["model"]

        if provider is None:
            # Último recurso: usar ChatOpenAI direto (OpenAI compatível)
            kwargs: dict[str, Any] = {"model": self.llm_model, "temperature": settings.AGENT_TEMPERATURE}
            if settings.OPENAI_API_BASE:
                kwargs["base_url"] = settings.OPENAI_API_BASE
            self.llm = ChatOpenAI(**kwargs)
        else:
            # Usar o provider via OpenAI-compatible endpoint
            base_url = getattr(provider, "base_url", None)
            if base_url:
                # Garantir que /v1 está no final para compatibilidade OpenAI
                openai_base_url = base_url.rstrip("/")
                if not openai_base_url.endswith("/v1"):
                    openai_base_url = f"{openai_base_url}/v1"
                self.llm = ChatOpenAI(
                    model=self.llm_model,
                    temperature=settings.AGENT_TEMPERATURE,
                    base_url=openai_base_url,
                    api_key="lm-studio",
                )
            else:
                # Provider não tem base_url OpenAI-compatible (ex: Groq via raw httpx)
                kwargs = {"model": self.llm_model, "temperature": settings.AGENT_TEMPERATURE}
                if settings.OPENAI_API_BASE:
                    kwargs["base_url"] = settings.OPENAI_API_BASE
                self.llm = ChatOpenAI(**kwargs)

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def _build_system_prompt(self) -> str:
        return settings.AGENT_SYSTEM_PROMPT_TEMPLATE.format(
            agent_name=self.agent_name,
            tenant_name=self.tenant_name,
            commercial_rules=self.commercial_rules,
            client_context="",
        )

    def _call_model(self, state: AgentState) -> dict:
        system_message = SystemMessage(content=self._build_system_prompt())
        messages = [system_message] + state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def _should_continue(self, state: AgentState) -> Literal["tools", END]:
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        return END

    def build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", self._should_continue, {"tools": "tools", END: END})
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    async def process_message(
        self,
        user_message: str,
        channel: str,
        history: list[dict] | None = None,
        context: dict | None = None,
    ) -> str:
        await self._setup_llm()
        self._model_manager.touch(self.llm_model)

        graph = self.build_graph()

        messages = []
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=user_message))

        initial_state: AgentState = {
            "messages": messages,
            "tenant_id": context.get("tenant_id", "") if context else "",
            "contact_id": context.get("contact_id", "") if context else "",
            "channel": channel,
            "context": context or {},
        }

        final_state = await graph.ainvoke(initial_state)
        last_message = final_state["messages"][-1]

        if isinstance(last_message, AIMessage):
            return last_message.content
        return str(last_message)
