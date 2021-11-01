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
  ITEM_CREATE_BY_FORM_MUTATION,
  ITEM_UPDATE_BY_FORM_MUTATION,
  doItemFetchById
} from '../graphql/Item.js'
import { fetchCategoryAll } from '../graphql/Category.js'
import ModelDetailView from '../components/ModelDetailView.vue'
import { getModelIdFromRoute, isModelIdNew } from '../components/Base.js'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, computed } from 'vue'

export default {
  name: 'ItemDetailView',
  setup () {
    const route = useRoute()
    const id = computed(() => getModelIdFromRoute(route))
    const isNew = computed(() => isModelIdNew(id.value))
    const loading = ref(false)
    const formData = ref({})
    const selectOptionData = ref({})
    const router = useRouter()

    const getItemById = async () => {
      loading.value = true
      const { onResult, isIdNotFound } = await doItemFetchById(id)
      onResult(result => {
        if (!isIdNotFound.value) {
          formData.value = result.data.itemById
          loading.value = false
        } else {
          loading.value = false
          router.replace({ name: 'notFound404' })
          loading.value = false
        }
      })
    }
    const getCategoryAll = async () => {
      loading.value = true
      selectOptionData.value.category = await fetchCategoryAll().data
      loading.value = false
    }
    onMounted(() => {
      if (!isNew.value) {
        getItemById()
      } else {
        formData.value = {
          name: '',
          category: { id: '' },
          sku: '',
          upc: '',
          price: 0,
          packQty: 0
        }
      }
      // To-do: getCategoryAll should not run when getItemById return empty
      // Tried async/await, computed, and watch for isIdNotFound flag but failed
      getCategoryAll()
    })
    return {
      id,
      isNew,
      formData,
      getItemById,
      loading,
      getCategoryAll,
      selectOptionData
    }
  },
  data: function () {
    return {
      MODEL_NAME: 'Item',
      MODEL_CREATE_BY_FORM_MUTATION: ITEM_CREATE_BY_FORM_MUTATION,
      createMutationFormDataId: 'itemCreateByForm',
      MODEL_UPDATE_BY_FORM_MUTATION: ITEM_UPDATE_BY_FORM_MUTATION,
      updateMutationFormDataId: 'itemUpdateByForm',
      formElement: {
        name: 'input-text',
        category: 'select-option',
        sku: 'input-text',
        upc: 'input-text',
        price: 'input-number',
        packQty: 'input-number'
      }
    }
  },
  components: {
    ModelDetailView
  },
  computed: {
    formDataMutation: function () {
      // copy formData object
      const data = { ...this.formData }
      // check to make sure data is not empty {} due to formData async not fecthed yet
      if (Object.keys(data).length > 0) {
        // pick category id for mutation
        data.category = data.category.id

        // rename packQty property to pack_qty for mutation
        data.pack_qty = data.packQty
        delete data.packQty
      }
      return data
    },
    createMutationVariables: function () {
      return {
        ItemFormCreateMutationInput: {
          ...this.formDataMutation
        }
      }
    },
    updateMutationVariables: function () {
      let ItemFormUpdateMutationInput = {}
      if (!this.isNew) {
        ItemFormUpdateMutationInput = Object.assign(
          ItemFormUpdateMutationInput,
          { id: parseInt(this.id) },
          this.formDataMutation
        )
      }
      return {
        ItemFormUpdateMutationInput: ItemFormUpdateMutationInput
      }
    }
  }
}
</script>
