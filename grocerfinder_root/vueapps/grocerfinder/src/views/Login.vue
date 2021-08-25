<template>
  <div id="grocerfinder">
    <form @submit.prevent="signIn">
      <label for="username"> Username</label>
      <input type="text" v-model.trim="username" id="username" />
      <br />
      <label for="password">Password</label>
      <input type="password" v-model.trim="password" id="password" />
      <br />
      <input type="submit" value="Sign in" />
    </form>
  </div>
</template>

<script>
import { TOKEN_AUTH_MUTATION } from '../graphql/Authentication.js'

export default {
  name: 'Login',
  data: function () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async signIn () {
      const data = await this.$apollo.mutate({
        mutation: TOKEN_AUTH_MUTATION,
        variables: {
          username: this.username,
          password: this.password
        }
      })
      console.log(data)
      window.location.reload()
    }
  }
}
</script>
