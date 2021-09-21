<template>
  <div v-if="!loading">
    <select name="" id="" v-model="sortByField">
      <option
        v-for="field in sortedFields"
        :key="field"
        :value="field"
        :selected="sortByField"
      >
        {{ field }}
      </option>
    </select>
    <select name="" id="" v-model="pageSize">
      <option
        v-for="size in pageSizeOption"
        :key="size"
        :value="size"
        :selected="pageSize"
      >
        {{ size }}
      </option>
    </select>
    <model-list-view
      v-if="!loading"
      :modelName="modelName"
      :modelData="itemData"
      :deleteMutation="deleteMutation"
      :refetch="refetch"
    >
    </model-list-view>
    <button @click="doFetchMore" class="btn btn-primary">Load More</button>
    <button @click="testThis" class="btn btn-danger">
      Test This from Parent Component
    </button>
  </div>
</template>

<script>
import { ITEM_DELETE_MUTATION, doItemFetchMore } from '../graphql/Item.js'

import ModelListView from '../components/ModelListView.vue'

import { ref, computed, watch } from 'vue'

export default {
  name: 'ItemListView',
  data () {
    return {
      modelName: 'Item',
      deleteMutation: ITEM_DELETE_MUTATION,
      sortedFields: ['id', 'price'],
      pageSizeOption: [5, 10, 25, 50, 100]
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
  setup () {
    const sortByField = ref('id')
    const pageSize = ref(5)
    const cursorInitial = 0
    const cursorIdInitial = 0
    const itemData = ref([])
    const {
      loading,
      refetch,
      onResult
      // fetchMore
    } = doItemFetchMore(
      cursorInitial,
      cursorIdInitial,
      pageSize.value,
      sortByField.value
    )
    onResult(result => {
      itemData.value.push(...result.data.itemFetchMore)
    })

    const cursor = computed(() => {
      return itemData.value[itemData.value.length - 1][sortByField.value]
    })
    const cursorId = computed(() => {
      return itemData.value[itemData.value.length - 1].id
    })
    function doFetchMore () {
      // this is fine but encounter:
      // runtime-core.esm-bundler.js:6873 [Vue warn]: onServerPrefetch is called when there is no active component instance to be associated with. Lifecycle injection APIs can only be used during execution of setup(). If you are using async setup(), make sure to register lifecycle hooks before the first await statement.
      // const { onResult } = doItemFetchMore(
      //   cursor.value,
      //   cursorId.value,
      //   pageSize.value,
      //   sortByField.value
      // )
      // onResult(result => {
      //   itemData.value.push(...result.data.itemFetchMore)
      // })

      refetch({
        cursor: String(cursor.value),
        cursor_id: cursorId.value,
        page_size: pageSize.value,
        sort_by_field: sortByField.value
      })
      // trying fetchMore https://v4.apollo.vuejs.org/guide-composable/pagination.html#cursor-based
      // fetchMore({
      //   variables: {
      //     cursor: String(cursor.value),
      //     cursor_id: cursorId.value,
      //     pageSize: pageSize.value,
      //     sort_by_field: sortByField.value
      //   },
      //   updateQuery: (_, { fetchMoreResult }) => {
      //     itemData.value.push(...fetchMoreResult.itemFetchMore)
      //   }
      // })
    }
    watch([pageSize, sortByField], (newValue, _) => {
      // this is fine but encounter:
      // runtime-core.esm-bundler.js:6873 [Vue warn]: onServerPrefetch is called when there is no active component instance to be associated with. Lifecycle injection APIs can only be used during execution of setup(). If you are using async setup(), make sure to register lifecycle hooks before the first await statement.
      const { onResult } = doItemFetchMore(
        cursorInitial,
        cursorIdInitial,
        newValue[0],
        newValue[1]
      )
      onResult(result => {
        itemData.value = result.data.itemFetchMore
      })
    })
    return {
      itemData,
      loading,
      sortByField,
      pageSize,
      cursor,
      cursorId,
      doFetchMore,
      refetch
    }
  }
}
</script>
