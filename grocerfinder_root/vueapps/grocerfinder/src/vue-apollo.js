import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option'

// HTTP connection to the API
const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: 'http://localhost:8000/graphql',
  credentials: 'include',
  headers: {}
})

// Cache implementation
const CACHE = new InMemoryCache()

const defaultOptions = {
  link: httpLink,
  cache: CACHE
}

// Create the apollo client
export const apolloClient = new ApolloClient({
  ...defaultOptions
})

// for apollo-option
export const apolloProvider = createApolloProvider({
  defaultClient: apolloClient,
  defaultOptions: {
    $query: {
      fetchPolicy: 'cache-and-network'
    }
  }
})
