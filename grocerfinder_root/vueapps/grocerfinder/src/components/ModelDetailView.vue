<template>
  <div>
    <model-form
      :modelName="modelNametoLowerCase"
      :formData="formData"
      @update:formData="updateFormData"
      :isNew="isNew"
      :selectOptionData="selectOptionData"
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
import ModelForm from './ModelForm.vue'

const _ = require('lodash')

export default {
  name: 'ModelDetailView',
  data: function () {
    return {
      nonFieldErrors: [],
      fieldErrors: {},
      hiddenErrors: [],
      okMessages: []
    }
  },
  components: {
    ModelForm
  },
  props: [
    'MODEL_NAME',
    'formData',
    'MODEL_CREATE_BY_FORM_MUTATION',
    'createMutationVariables',
    'createMutationFormDataId',
    'MODEL_UPDATE_BY_FORM_MUTATION',
    'updateMutationVariables',
    'updateMutationFormDataId',
    'selectOptionData',
    'formElement',
    'isNew'
  ],
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
      } else {
        // No Error
        let ok
        if (this.isNew) {
          ok = this.modelNametoLowerCase + ' added OK'
          // redirect to <model>/:id/ route
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
    },
    updateFormData (key, value) {
      _.set(this.formData, key, value)
    }
  },
  computed: {
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
