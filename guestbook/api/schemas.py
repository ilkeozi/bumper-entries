from drf_yasg import openapi

error_detail_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "field": openapi.Schema(type=openapi.TYPE_STRING, description="Field name where validation failed"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Validation error message"),
    }
)

error_response = openapi.Response(
    description="Validation error",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=error_detail_schema,
                description="List of validation errors with field and message details"
            )
        }
    )
)
