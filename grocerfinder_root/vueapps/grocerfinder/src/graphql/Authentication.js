
import gql from 'graphql-tag'

export const USER_IDENTITY_QUERY = gql`
  query me {
    userIdentityObject: me {
      username
      firstName: first_name
      lastName: last_name
    }
  }
`

export const REFRESH_TOKEN_MUTATION = gql`
  mutation refresh_token {
    refresh_token {
      token
    }
  }
`

export const TOKEN_AUTH_MUTATION = gql`
  mutation token_auth($username: String!, $password: String!) {
    tokenAuth: token_auth(username: $username, password: $password) {
      token
      payload
      refreshToken: refresh_token
      refreshExpiresIn: refresh_expires_in
    }
  }
`

export const DELETE_TOKEN_COOKIE_MUTATION = gql`
  mutation delete_token_cookie{
    deleteTokenCookie: delete_token_cookie {
      __typename
    }
  }
`
