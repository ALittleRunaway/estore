from estore.domain.entity.user import User
from typing import Union


class UserGateway():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def authorise(self, login, password) -> Union[User, None]:
        query = f"""
        SELECT u.id, u.name, u.surname, u.patronymic, r.display_name, r.id
        FROM estore.user u
        INNER JOIN estore.role r ON u.role_id = r.id
            WHERE login = '{login}' AND password = '{password}';
        """

        res = [list(x) for x in self.db_conn.execute(query).fetchall()]
        if len(res) == 0:
            return None
        return User(
            id=res[0][0],
            name=res[0][1],
            surname=res[0][2],
            patronymic=res[0][3],
            role=res[0][4],
            role_id=res[0][5],
        )
