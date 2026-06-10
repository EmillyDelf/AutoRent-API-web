from django.http import JsonResponse


def home(request):
    """
    View temporária do projeto AutoRent.

    Neste momento o foco do projeto está na
    implementação do backend e das regras de negócio.

    Futuramente um front-end React poderá consumir
    a API REST que será desenvolvida.

    Esta rota existe apenas para validar que a aplicação
    está funcionando corretamente.
    """

    return JsonResponse({
        "projeto": "AutoRent",
        "status": "online",
        "versao": "1.0",
        "mensagem": (
            "Backend funcionando corretamente. "
            "A API REST será implementada posteriormente."
        )
    })


def health_check(request):
    """
    Endpoint simples para verificar se o servidor
    está operacional.

    Pode ser utilizado futuramente por:
    - React
    - Docker

    Não depende de banco de dados.
    """

    return JsonResponse({
        "status": "ok"
    })