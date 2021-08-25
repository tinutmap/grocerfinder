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
      const data = await this.$apollo.mutate({
        mutation: DELETE_TOKEN_COOKIE_MUTATION
      })
      console.log(data)
      localStorage.userIdentity = ''
      window.location.reload()
    }
  }
}
</script>
