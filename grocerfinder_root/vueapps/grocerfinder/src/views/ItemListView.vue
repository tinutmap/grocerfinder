<template>
  <div>
    <model-list-view
      :modelName="modelName"
      :deleteMutation="deleteMutation"
      :sortedFields="sortedFields"
      :doModelFetchMore="doModelFetchMore"
    >
    </model-list-view>
  </div>
</template>

<script>
import { ITEM_DELETE_MUTATION, doItemFetchMore } from '../graphql/Item.js'

import ModelListView from '../components/ModelListView.vue'

export default {
  name: 'ItemListView',
  data () {
    return {
      modelName: 'Item',
      deleteMutation: ITEM_DELETE_MUTATION,
      sortedFields: ['id', 'price'],
      doModelFetchMore: doItemFetchMore
    }
  },
  components: {
    ModelListView
  },
  computed: {},
  setup () {}
}
</script>
