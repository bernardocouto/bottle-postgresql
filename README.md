# Bottle PostgreSQL
Bottle PostgreSQL is a simple adapter for PostgreSQL with connection pooling.

## Configuration
The configuration can be done through **JSON** file or by **Dict** following the pattern described below:
```json
{
  "database": "postgres",
  "host": "localhost",
  "max_connection": 10,
  "password": "postgres",
  "port": 5432,
  "print_sql": true,
  "username": "postgres"
}
```

Create the `queries` directory. This should contain all the `.sql` files that the library will use.

## Usage
PyPostgreSQLWrapper usage description:

### Delete

#### Delete with where
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .delete('test')
        .where('id', 1)
        .execute()
    )
```

#### Delete with where condition
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .delete('test')
        .where('description', 'Test%', operator='like')
        .execute()
    )
```

### Execute
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .execute(
            '''
                create table if not exists test (
                    id bigserial not null,
                    name varchar(100),
                    description varchar(255),
                    constraint test_primary_key primary key (id)
                )
            ''',
            skip_load_query=True
        )
    )
```

### Insert
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .insert('test')
        .set('id', 1)
        .set('name', 'Name')
        .set('description', 'Description')
        .execute()   
    )
```

### Paging

#### Paging with where condition
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .select('test')
        .fields('id', 'name', 'description')
        .where('id', 1, operator='>')
        .order_by('id')
        .paging(0, 2)
    )
```

#### Paging without where condition
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .select('test')
        .paging(0, 10)
    )
```

### Select

#### Fetch all
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .select('test')
        .execute()
        .fetch_all()   
    )
```

#### Fetch many
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .select('test')
        .execute()
        .fetch_many(1)
    )
```

#### Fetch one
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .select('test')
        .execute()
        .fetch_one()
    )
```

#### Select by file
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .execute('find_by_id', {'id': 1})
        .fetch_one()
    )
```

#### Select by query
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .execute('select id, name, description from test where id = %(id)s', {'id': 1})
        .fetch_one()
    )
```

### Update

#### Update with where
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .update('test')
        .set('name', 'New Name')
        .set('description', 'New Description')
        .where('id', 1)
        .execute()   
    )
```

#### Update with where all
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .update('test')
        .set('name', 'New Name')
        .set('description', 'New Description')
        .where_all({'id': 1, 'name': 'Name', 'description': 'Description'})
        .execute()
    )
```

### Using filters

#### SQL
```sql
select
    id,
    name,
    description
from test
where 1 = 1
{{#id}}
and id = %(id)s
{{/id}}
{{#id}}
and name like %(name)s
{{/id}}
```

#### Select with filters
```python
from bottle_postgresql import Database

with Database() as connection:
    (
        connection
        .execute('test.find_all_with_filter', parameters={'id': 1, 'name': 'Name'})
        .fetch_one()
    )
```
