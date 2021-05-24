class Schema:

    BODY = 'body'
    QUERY_PARAMETER = 'query_parameter'
    URL_PARAMETER = 'url_parameter'

    @staticmethod
    def validate_body(schema):
        return {Schema.BODY: schema()}

    @staticmethod
    def validate_query_parameter(schema):
        return {Schema.QUERY_PARAMETER: schema()}

    @staticmethod
    def validate_url_parameter(schema):
        return {Schema.URL_PARAMETER: schema()}
