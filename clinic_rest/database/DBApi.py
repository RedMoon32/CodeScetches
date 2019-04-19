import redis
from redis.exceptions import ConnectionError
import os

class Connection:
    db = os.environ.get('DATA_BASE')

    def __init__(self, host=db if db else 'localhost', port='6379'):
        print(host)
        try:
            self.client = redis.Redis(host=host, port=port, decode_responses=True)
            self.client.set('test', 'testing')
            self.client.delete('test')
            self.connected = True
        except ConnectionError:
            self.connected = False
            print('Redis Server is unreachable')

db_connection = Connection()

class DBEntity:
    def __init__(self, dbid: str):
        self.type = self.__class__.__name__.lower()
        self.id = dbid
        self.key = self.type + ':' + self.id

    def save(self, con: Connection):
        if not con.client.exists(self.key):

            class_fields = self.__dict__.copy()
            del class_fields['key']

            # Foreign keys, int, bool type handling
            for field_key in class_fields:
                field_value = class_fields[field_key]
                if isinstance(field_value, ForeignKey):
                    con.client.sadd('one_to_many:' + field_value.key + ':' + self.type, self.key)
                    class_fields[field_key] = field_value.key

                if isinstance(field_value, (int, bool)):
                    class_fields[field_key] = str(class_fields[field_key])

            con.client.hmset(self.key, class_fields)

            return True
        else:
            return False

    @classmethod
    def get_by_key(cls, key, con):
        id = key.split(':')[1]
        if con.client.exists(key):

            entity = cls(id)

            class_fields = entity.__dict__
            db_entity = con.client.hgetall(key)
            class_fields['key'] = key
            class_fields['id'] = id

            # Push values from db into entity
            for key in db_entity:
                class_field_value = class_fields[key]
                if isinstance(class_field_value, ForeignKey):
                    class_fields[key] = ForeignKey(db_entity[key])
                elif isinstance(class_field_value, int):
                    class_fields[key] = int(db_entity[key])
                elif isinstance(class_field_value, bool):
                    class_fields[key] = bool(db_entity[key])
                else:
                    class_fields[key] = db_entity[key]

            return entity
        else:
            return None

    @classmethod
    def get_by_id(cls, dbid, con):
        key = cls.__name__.lower() + ':' + dbid
        if con.client.exists(key):

            entity = cls(dbid)

            class_fields = entity.__dict__
            db_entity = con.client.hgetall(key)
            class_fields['key'] = key

            # Push values from db into entity
            for key in db_entity:
                class_field_value = class_fields[key]
                if isinstance(class_field_value, ForeignKey):
                    class_fields[key] = ForeignKey(db_entity[key])
                elif isinstance(class_field_value, int):
                    class_fields[key] = int(db_entity[key])
                elif isinstance(class_field_value, bool):
                    class_fields[key] = bool(db_entity[key])
                else:
                    class_fields[key] = db_entity[key]

            return entity
        else:
            return None

    def delete(self, connection: Connection):
        if connection.client.delete(self.key) != 0:

            # For indexing correctness by another DBEntities
            class_fields = self.__dict__.copy()

            # Foreign keys, int, bool type handling
            for field_key in class_fields:
                field_value = class_fields[field_key]
                if isinstance(field_value, ForeignKey):
                    connection.client.srem('one_to_many:' + field_value.key + ':' + self.type, self.key)

            return True
        else:
            return False

    @classmethod
    def get_all(cls, connection):
        entity_list = []
        all_keys = connection.client.keys(cls.__name__.lower() + ':*')
        for entity_key in all_keys:
            entity = cls.get_by_key(entity_key, connection)
            entity_list.append(entity)
        return entity_list

    # @staticmethod
    # def get_type_by_id(id, con: Connection):
    #     string = con.client.keys('*:' + id)
    #     if len(string) == 1:
    #         string = string[0]
    #         string.split(':')
    #         return string.split(':')[0]


class ForeignKey:

    def __init__(self, key):
        self.key = key
        self.id = key.split(':')[1]


def get_seconds_from_midnight():
    import datetime
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    return seconds
