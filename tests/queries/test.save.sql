insert into test (
    name,
    description
) values (
    %(name)s,
    %(description)s
)
returning *
