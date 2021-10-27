<template>
  <div v-if="userIdentity === 'Guest'">
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
  <div v-else>
    <h1>User already logged in.</h1>
    <button @click="redirectPath">Redirect</button>
  </div>
</template>

<script>
import { TOKEN_AUTH_MUTATION } from '../graphql/Authentication.js'
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
    redirectPath () {
      // redirect to route next query or root uri
      const nextPath = this.$route.query.next || '/'
      this.doRefetchUserIdentity()
      this.$router.push(nextPath)
    },
    async signIn () {
      await this.$apollo.mutate({
        mutation: TOKEN_AUTH_MUTATION,
        variables: {
          username: this.username,
          password: this.password
        }
      })
      this.redirectPath()
    }
  },
  setup () {
    const doRefetchUserIdentity = inject('doRefetchUserIdentity')
    const userIdentity = inject('userIdentity')
    return { doRefetchUserIdentity, userIdentity }
  }
}
</script>
