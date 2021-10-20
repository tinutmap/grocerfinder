import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option'

// HTTP connection to the API
const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: process.env.VUE_APP_API_ENDPOINT,
  credentials: 'include',
  headers: {}
})

// Cache implementation
const CACHE = new InMemoryCache({
  addTypename: false
})

const defaultOptions = {
  link: httpLink,
  cache: CACHE,
  query: {
    // use { fetchPolicy: 'no-cache' } in order to mutate the result used at input form
    // https://github.com/apollographql/apollo-client/issues/5903
    // To-do: write update cache function
    // fetchPolicy: 'cache-and-network'
    fetchPolicy: 'no-cache'
  }
}

// Create the apollo client
export const apolloClient = new ApolloClient({
  ...defaultOptions
})

// for apollo-option
export const apolloProvider = createApolloProvider({
  defaultClient: apolloClient
  // defaultOptions: {
  //   $query: {
  //     // fetchPolicy: 'cache-and-network'
  //     fetchPolicy: 'no-cache'
  //   }
  // }
})
