<template>
  <div id="logout-button">
    <input
      type="button"
      value="Log Out"
      @click="logOut()"
      class="btn btn-warning"
    />
  </div>
</template>

<script>
import { DELETE_TOKEN_COOKIE_MUTATION } from '../graphql/Authentication.js'
import { inject } from 'vue'
export default {
  name: 'Login',
  data: function () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async logOut () {
      await this.$apollo.mutate({
        mutation: DELETE_TOKEN_COOKIE_MUTATION
      })
      this.doRefetchUserIdentity()
    }
  },
  setup () {
    const doRefetchUserIdentity = inject('doRefetchUserIdentity')
    return { doRefetchUserIdentity }
  }
}
</script>
