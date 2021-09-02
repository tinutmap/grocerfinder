<template>
  <model-list-view
    v-if="!loading"
    :modelName = "modelName"
    :modelData = "allCategoriesDateTimeUpdatedCast"
    :deleteMutation="deleteMutation"
    :refetch = "refetch"
  >
</model-list-view>
</template>

<script>
import {
  CATEGORY_DELETE_MUTATION,
  fetchCategoryAll
} from '../graphql/Category.js'

import ModelListView from '../components/ModelListView.vue'

export default {
  name: 'CategoryListView',
  data () {
    return {
      modelName: 'Category',
      deleteMutation: CATEGORY_DELETE_MUTATION
    }
  },
  components: {
    ModelListView
  },
  methods: {
  },
  computed: {
    allCategoriesDateTimeUpdatedCast: function () {
      // cast datetimeUpdated from String to ISOString
      const t = this.data
      t.map(i => (i.datetimeUpdated = new Date(i.datetimeUpdated).toString()))
      return t
    }
  },
  setup () {
    const { data, loading, refetch } = fetchCategoryAll()
    return { data, loading, refetch }
  }
}
</script>
