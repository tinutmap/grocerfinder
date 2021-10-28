
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { ref } from 'vue'

export const USER_IDENTITY_QUERY = gql`
  query me {
    userIdentityObject: me {
      username
      firstName: first_name
      lastName: last_name
    }
  }
`

export function doUserIdentityQuery () {
  const { onResult, refetch, restart, onError } = useQuery(USER_IDENTITY_QUERY,
    { fetchPolicy: 'no-cache' }
  )
  // default value 'Guest' if onResult not run
  const userIdentity = ref('Guest')
  onResult(result => {
    try {
      result = result.data.userIdentityObject
      userIdentity.value = result.firstName || result.username
      // eslint-disable-next-line no-empty
    } catch (e) { }
  })
  onError(_ => {
    // Rest userIdentity to 'Guest' when query fails, e.g. not Logged in or Logged out
    userIdentity.value = 'Guest'
  })
  return { userIdentity, refetch, restart }
}

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
