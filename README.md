# users-service

[![Coverage Status](https://coveralls.io/repos/github/classconnect-grupo3/users-service/badge.svg?branch=testing-and-ci)](https://coveralls.io/github/classconnect-grupo3/users-service?branch=testing-and-ci)


# Endpoints

| **Endpoint**          | **Descripción**                     | **Método HTTP** | **URL**                     |
|------------------------|-------------------------------------|-----------------|-----------------------------|
| `/register`           | Crear un nuevo usuario.            | `POST`          | `https://users-service-production-968d.up.railway.app/docs#/register/create_user_register_post` |
| `/login`              | Iniciar sesión con email y contraseña. | `POST`          | `https://users-service-production-968d.up.railway.app/docs#/login/login_user_login_post`    |
| `/users/me/location`  | Almacenar la ubicación del usuario. | `POST`          | `https://users-service-production-968d.up.railway.app/docs#/users/store_user_location_users_me_location_post` |

---

## Ejemplo de Uso

### 1. **Crear un Nuevo Usuario**
- **URL**: `https://users-service-production-968d.up.railway.app/docs#/register/create_user_register_post`
- **Método**: `POST`
- **Cuerpo de la Solicitud**:
    ```json
    {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword"
    }
    ```
- **Respuesta Exitosa**:
    ```json
    {
        "data": {
            "uid": "unique-user-id",
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "location": null
        }
    }
    ```

---

### 2. **Iniciar Sesión**
- **URL**: `https://users-service-production-968d.up.railway.app/docs#/login/login_user_login_post`
- **Método**: `POST`
- **Cuerpo de la Solicitud**:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "securepassword"
    }
    ```
- **Respuesta Exitosa**:
    ```json
    {
        "id_token": "jwt-token",
        "user_location": Optional[str]
    }
    ```

---

### 3. **Almacenar la Ubicación del Usuario**
- **URL**: `https://users-service-production-968d.up.railway.app/docs#/users/store_user_location_users_me_location_post`
- **Método**: `POST`
- **Cuerpo de la Solicitud**:
    ```json
    {
        "country": "Argentina"
    }
    ```
- **Respuesta Exitosa**:
    ```json
    {
        200 OK
    }
    ```

