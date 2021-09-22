<template>
  <div>
    <model-list-view
      :modelName="modelName"
      :deleteMutation="deleteMutation"
      :sortedFields="sortedFields"
      :doModelFetchMore="doModelFetchMore"
    >
    </model-list-view>
    <button @click="testThis" class="btn btn-danger">
      Test This from Parent Component
    </button>
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
  methods: {
    testThis () {
      console.log(this)
    }
  },
  computed: {},
  setup () {}
}
</script>
