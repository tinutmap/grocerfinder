<template>
  <div id="grocerfinder">
    <!-- <apolloCompCategory /> -->
    <header>
      <router-link to="/">
        <h1>Grocerfinder Home</h1>
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
      <router-view />
      <!-- <all-items /> -->
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
/* @import "~@/assets/scss/vendors/bootstrap-vue/index"; */
@import "bootstrap";

.error-field {
  @extend .text-danger;
}
</style>
