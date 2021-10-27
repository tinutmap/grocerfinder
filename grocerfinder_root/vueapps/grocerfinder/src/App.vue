<template>
  <div>
    <header>
      <router-link to="/">
        <h1>Grocerfinder Home</h1>
      </router-link>
      <router-link to="/category">
        <h2>Category</h2>
      </router-link>
      {{ userIdentity }}<br />
      <div v-if="userIdentity === 'Guest'">
        <router-link :to="'/login/?next=' + $route.path">Login</router-link>
      </div>
      <div v-else>
        <logout-button />
      </div>
    </header>
    <body>
      <router-view></router-view>
    </body>
  </div>
</template>

<script>
import LogoutButton from './components/LogoutButton.vue'
import { doUserIdentityQuery } from './graphql/Authentication.js'
import { provide } from 'vue'
export default {
  name: 'grocerfinder',
  components: {
    LogoutButton
  },
  setup () {
    const { userIdentity, refetch, restart } = doUserIdentityQuery()
    const doRefetchUserIdentity = () => {
      // restart() the query so refetch() will hit onResult hook
      restart()
      refetch()
    }
    provide('doRefetchUserIdentity', doRefetchUserIdentity)
    provide('userIdentity', userIdentity)
    return { userIdentity, refetch, doRefetchUserIdentity }
  }
}
</script>

<style lang="scss">
@import "bootstrap";
.error-field {
  @extend .text-danger;
}
</style>
