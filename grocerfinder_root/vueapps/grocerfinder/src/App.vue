<template>
  <div>
    <header>
      <router-link to="/">
        <img src="../public/favicon_title_2.png" alt="" />
      </router-link>
      <router-link to="/item">
        <h2>Item</h2>
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
// import HelloWorld from './components/HelloWorld.vue'
export default {
  name: 'grocerfinder',
  components: {
    LogoutButton
    // HelloWorld
  },
  setup () {
    const { userIdentity, refetch } = doUserIdentityQuery()
    const doRefetchUserIdentity = () => {
      refetch()
    }
    provide('doRefetchUserIdentity', doRefetchUserIdentity)
    provide('userIdentity', userIdentity)
    return { userIdentity, refetch }
  }
}
</script>

<style lang="scss">
@import "bootstrap";
.error-field {
  @extend .text-danger;
}
</style>
