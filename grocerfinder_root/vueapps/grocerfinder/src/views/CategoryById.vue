<script>
import {
  categoryByIdQueryData,
  CATEGORY_CREATE_BY_FORM_MUTATION,
  CATEGORY_UPDATE_BY_FORM_MUTATION
} from '../graphql/Category.js'
import ModelByIdMixins from './ModelByIdMixins.vue'

export default {
  name: 'CategoryById',
  mixins: [ModelByIdMixins],
  data: function () {
    return {
      MODEL_NAME: 'Category',
      formData: { name: '' },
      MODEL_CREATE_BY_FORM_MUTATION: CATEGORY_CREATE_BY_FORM_MUTATION,
      createMutationFormDataId: 'categoryCreateByForm',
      MODEL_UPDATE_BY_FORM_MUTATION: CATEGORY_UPDATE_BY_FORM_MUTATION,
      updateMutationFormDataId: 'categoryUpdateByForm',
      formElement: {
        name: 'input-text'
      }
    }
  },
  async created () {
    if (!this.isNew) {
      this.loading = true
      const data = await categoryByIdQueryData(parseInt(this.id))
      if (data.data) {
        this.formData = data.data
        // this.nonFieldErrors = data.errors;
        this.loading = false
      } else {
        this.$router.replace({ name: 'notFound404' })
      }
    }
  },
  methods: {},
  computed: {
    createMutationVariables: function () {
      return {
        CategoryFormCreateMutationInput: {
          ...this.formDataMutation
        }
      }
    },
    updateMutationVariables: function () {
      let CategoryFormUpdateMutationInput = {}
      if (!this.isNew) {
        CategoryFormUpdateMutationInput = Object.assign(
          CategoryFormUpdateMutationInput,
          { id: parseInt(this.id) },
          this.formDataMutation
        )
      }
      return {
        CategoryFormUpdateMutationInput: CategoryFormUpdateMutationInput
      }
    }
  }
}
</script>
