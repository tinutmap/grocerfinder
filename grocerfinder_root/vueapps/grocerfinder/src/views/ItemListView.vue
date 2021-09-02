<template>
  <div>
<model-list-view
    v-if="!loading"
    :modelName = "modelName"
    :modelData = "data"
    :deleteMutation="deleteMutation"
    :refetch = "refetch"
  >
</model-list-view>
      <button @click="testThis" class="btn btn-danger">
        Test This from Parent Component
      </button>
  </div>

</template>

<script>
import {
  ITEM_DELETE_MUTATION,
  fetchItemAll
} from '../graphql/Item.js'

import ModelListView from '../components/ModelListView.vue'

export default {
  name: 'ItemListView',
  data () {
    return {
      modelName: 'Item',
      deleteMutation: ITEM_DELETE_MUTATION
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
  setup () {
    const { data, loading, refetch } = fetchItemAll()
    return { data, loading, refetch }
  }
}
</script>
