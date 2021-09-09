<template>
  <div>
    <header>
      <router-link to="/">
        <h1>Grocerfinder Home</h1>
      </router-link>
      <router-link to="/category">
        <h2>Category</h2>
      </router-link>
      {{ userIdentity || "Guest" }}
      <div v-if="!userIdentity">
        <router-link to="/login/">Login</router-link>
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
import { USER_IDENTITY_QUERY } from './graphql/Authentication.js'

export default {
  name: 'grocerfinder',
  components: {
    LogoutButton
  },
  data: function () {
    return {
      userIdentity: ''
    }
  },

  async created () {
    try {
      const data = await this.$apollo.query({
        query: USER_IDENTITY_QUERY
      })
      if (data) {
        this.userIdentity =
          data.data.userIdentityObject.firstName ||
          data.data.userIdentityObject.username
      }
    } catch (e) {
      console.log('User not logged in.', e.message)
    }
  },

  methods: {},
  computed: {}
}
</script>

<style lang="scss">
@import "bootstrap";
.error-field {
  @extend .text-danger;
}
</style>
