select
    id,
    name,
    description
from test
where 1 = 1
{{#id}}
and id = %(id)s
{{/id}}
{{#name}}
and name like %(name)s
{{/name}}
