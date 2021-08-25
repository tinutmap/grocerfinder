<script>
import {
  itemByIdQueryData,
  ITEM_CREATE_BY_FORM_MUTATION,
  ITEM_UPDATE_BY_FORM_MUTATION
} from '../graphql/Item.js'
import { categoryAllQueryData } from '../graphql/Category.js'
import ModelByIdMixins from './ModelByIdMixins.vue'

export default {
  name: 'ItemById',
  mixins: [ModelByIdMixins],
  data: function () {
    return {
      MODEL_NAME: 'Item',
      formData: {
        name: '',
        category: { id: '' },
        sku: '',
        upc: '',
        price: '',
        packQty: ''
      },
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
  async created () {
    this.loading = true
    const categoryAllData = await categoryAllQueryData()
    if (categoryAllData.data) {
      this.selectOptionData.category = categoryAllData.data
    }
    if (!this.isNew) {
      const data = await itemByIdQueryData(parseInt(this.id))
      if (data.data) {
        this.formData = data.data
        // this.nonFieldErrors = data.errors;
      } else {
        // https://github.com/vuejs/vue-router/issues/724 for fixing warning
        this.$router.replace({ name: 'notFound404' })
        // this.$router.replace({ path: "*/notFound404" });
        // this.$router.next({name: 'notFound404', params: {to.path, replace: true })
      }
    }
    this.loading = false
  },
  computed: {
    formDataMutation: function () {
      // shallow copy formData object
      const d = { ...this.formData }
      // pick category id for mutation
      d.category = d.category.id
      // // still need to parse price and pack_qty to Float although input type="number"
      // d.price = parseFloat(d.price) || 0;
      // d.pack_qty = parseFloat(d.packQty) || 0;
      d.pack_qty = d.packQty
      // packQty redundant with pack_qty => delete packQty
      delete d.packQty
      return d
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
