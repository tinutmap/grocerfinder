<template>
  <model-list-view
    :modelName="modelName"
    :deleteMutation="deleteMutation"
    :sortedFields="sortedFields"
    :doModelFetchMore="doModelFetchMore"
  >
  </model-list-view>
</template>

<script>
import {
  CATEGORY_DELETE_MUTATION,
  doCategoryFetchMore
} from '../graphql/Category.js'

import ModelListView from '../components/ModelListView.vue'

export default {
  name: 'CategoryListView',
  data () {
    return {
      modelName: 'Category',
      deleteMutation: CATEGORY_DELETE_MUTATION,
      sortedFields: ['id', 'name', 'datetime_updated'],
      doModelFetchMore: doCategoryFetchMore
    }
  },
  components: {
    ModelListView
  },
  methods: {},
  computed: {
    // allCategoriesDateTimeUpdatedCast: function () {
    //   // cast datetimeUpdated from String to ISOString
    //   const t = this.data
    //   t.map(i => (i.datetimeUpdated = new Date(i.datetimeUpdated).toString()))
    //   return t
    // }
  },
  setup () {}
}
</script>
