import {
  createApp,
  //  provide,
  h
} from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import { apolloClient, apolloProvider } from './vue-apollo'
import {
  // DefaultApolloClient,
  provideApolloClient
} from '@vue/apollo-composable'

const app = createApp({
  setup () {
    // provide(DefaultApolloClient, apolloClient)
    provideApolloClient(apolloClient)
  },
  render: () => h(App)
})

app.use(store).use(router).use(apolloProvider).mount('#app')
