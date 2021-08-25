<template>
  <div v-if="!loading">
    <model-form
      :modelName="modelNametoLowerCase"
      :formData="formData"
      :isNew="isNew"
      :selectOptionData="selectOptionData"
      :loading="loading"
      :formElement="formElement"
      :nonFieldErrors="nonFieldErrors"
      :fieldErrors="fieldErrors"
      :hiddenErrors="hiddenErrors"
      :okMessages="okMessages"
      @create="
        createUpdateMutation(
          MODEL_CREATE_BY_FORM_MUTATION,
          createMutationVariables,
          createMutationFormDataId
        )
      "
      @update="
        createUpdateMutation(
          MODEL_UPDATE_BY_FORM_MUTATION,
          updateMutationVariables,
          updateMutationFormDataId
        )
      "
    ></model-form>
  </div>
</template>
<script>
import ModelForm from '../components/ModelForm.vue'

export default {
  name: 'ModelByIdMixins',
  data: function () {
    return {
      MODEL_NAME: '', // filled by mixed Component
      formData: {}, // filled by mixed Component
      loading: false,
      MODEL_CREATE_BY_FORM_MUTATION: '', // filled by mixed Component
      createMutationFormDataId: '', // filled by mixed Component
      MODEL_UPDATE_BY_FORM_MUTATION: '', // filled by mixed Component
      updateMutationFormDataId: '', // filled by mixed Component
      selectOptionData: {}, // filled by mixed Component
      formElement: {}, // filled by mixed Component
      nonFieldErrors: [],
      fieldErrors: {},
      hiddenErrors: [],
      okMessages: []
    }
  },
  components: {
    ModelForm
  },

  methods: {
    processMutationData (data) {
      // reset errors and messages
      this.nonFieldErrors = []
      this.fieldErrors = {}
      this.hiddenErrors = []
      this.okMessages = []

      if (this.$apollo.error) {
        this.hiddenErrors = this.hiddenErrors.concat(data.errors)
      } else if (data.errors.length > 0) {
        for (let i = 0; i < data.errors.length; i++) {
          Object.defineProperty(this.fieldErrors, data.errors[i].field, {
            value: data.errors[i].messages,
            enumerable: true,
            writable: true
          })
        }
      } else { // No Error
        let ok
        if (this.isNew) {
          ok = this.modelNametoLowerCase + ' added OK'
          // redirect to item/:id/ route
          this.$router.replace({
            params: { id: data[this.modelNametoLowerCase].id }
          })
        } else {
          ok = this.modelNametoLowerCase + ' updated OK'
        }
        console.log(ok)
        this.okMessages.push(ok)
      }
    },
    async createUpdateMutation (mutation, variables, formDataId) {
      await this.$apollo
        .mutate({
          mutation: mutation,
          variables: variables
        })
        .then(data => this.processMutationData(data.data[formDataId]))
        .catch(e => {
          console.log(e)
          this.hiddenErrors.push(e)
        })
    }
  },
  computed: {
    // this.$route.params.id is string with either 'create' or 'id'
    // Need to cast to Int later if indeed a int
    id: function () {
      return this.$route.params.id
    },
    // return true if itemId is "new" string and false otherwise, i.e. an id
    isNew: function () {
      return typeof this.id === 'string'
        ? this.id.toLowerCase() === 'create'
        : false
    },

    // Force MODEL_NAME to lowercase to ensure consistent Object property lookup from fetched data.
    modelNametoLowerCase: function () {
      return this.MODEL_NAME.toLowerCase()
    },
    // this function is used when changing formData is needed
    // e.g. Change data property from camelCase to snake_case packQty => pack_qty
    // e.g. parseInt(id) to make sure id is Int
    // filled by mixed Component
    formDataMutation: function () {
      return this.formData
    }
  }
}
</script>
