<template>
  <model-detail-view
    v-if="!loading"
    :MODEL_NAME="MODEL_NAME"
    :formData="formData"
    :MODEL_CREATE_BY_FORM_MUTATION="MODEL_CREATE_BY_FORM_MUTATION"
    :createMutationVariables="createMutationVariables"
    :createMutationFormDataId="createMutationFormDataId"
    :MODEL_UPDATE_BY_FORM_MUTATION="MODEL_UPDATE_BY_FORM_MUTATION"
    :updateMutationVariables="updateMutationVariables"
    :updateMutationFormDataId="updateMutationFormDataId"
    :selectOptionData="selectOptionData"
    :formElement="formElement"
    :isNew="isNew"
  ></model-detail-view>
</template>
<script>
import {
  CATEGORY_CREATE_BY_FORM_MUTATION,
  CATEGORY_UPDATE_BY_FORM_MUTATION,
  fetchCategoryById
} from '../graphql/Category.js'
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getModelIdFromRoute, isModelIdNew } from '../components/Base.js'
import ModelDetailView from '../components/ModelDetailView.vue'

export default {
  name: 'CategoryDetailView',
  setup () {
    const route = useRoute()
    const id = computed(() => getModelIdFromRoute(route))
    const isNew = computed(() => isModelIdNew(id.value))
    const loading = ref(false)
    const formData = ref({})
    const router = useRouter()
    const selectOptionData = ref({})

    const getCategoryById = async () => {
      loading.value = true
      const { onResult, isIdNotFound } = await fetchCategoryById(id)
      onResult(result => {
        if (!isIdNotFound.value) {
          formData.value = result.data.categoryById
          loading.value = false
        } else {
          loading.value = false
          router.replace({ name: 'notFound404' })
          loading.value = false
        }
      })
    }
    onMounted(() => {
      if (!isNew.value) {
        getCategoryById()
      } else {
        formData.value = {
          name: ''
        }
      }
    })
    return { id, isNew, formData, getCategoryById, loading, selectOptionData }
  },
  data: function () {
    return {
      MODEL_NAME: 'Category',
      MODEL_CREATE_BY_FORM_MUTATION: CATEGORY_CREATE_BY_FORM_MUTATION,
      createMutationFormDataId: 'categoryCreateByForm',
      MODEL_UPDATE_BY_FORM_MUTATION: CATEGORY_UPDATE_BY_FORM_MUTATION,
      updateMutationFormDataId: 'categoryUpdateByForm',
      formElement: {
        name: 'input-text'
      }
    }
  },
  components: { ModelDetailView },
  computed: {
    formDataMutation: function () {
      return this.formData
    },
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
