<template>
  <div v-if="!loading">
    <model-list-view
      v-if="!loading"
      :modelName="modelName"
      :modelData="itemData"
      :deleteMutation="deleteMutation"
      :refetch="refetch"
      @doFetchMore="doFetchMore"
      :sortedFields="sortedFields"
      :sortByField="sortByField"
      @update:sortByField="updateFromChild($event, 'sortByField')"
      :pageSize="pageSize"
      @update:pageSize="updateFromChild($event, 'pageSize')"
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

import { ref, computed, watch } from 'vue'

export default {
  name: 'ItemListView',
  data () {
    return {
      modelName: 'Item',
      deleteMutation: ITEM_DELETE_MUTATION,
      sortedFields: ['id', 'price']
    }
  },
  components: {
    ModelListView
  },
  methods: {
    testThis () {
      console.log(this)
    },
    updateFromChild (event, variable) {
      this[variable] = event
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
      data,
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
    onResult(_ => {
      // itemData.value.push(...result.data.itemFetchMore)
      itemData.value.push(...data.value)
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
    watch([pageSize, sortByField], newValue => {
      // this is fine but encounter:
      // runtime-core.esm-bundler.js:6873 [Vue warn]: onServerPrefetch is called when there is no active component instance to be associated with. Lifecycle injection APIs can only be used during execution of setup(). If you are using async setup(), make sure to register lifecycle hooks before the first await statement.
      const { data, onResult } = doItemFetchMore(
        cursorInitial,
        cursorIdInitial,
        newValue[0],
        newValue[1]
      )
      onResult(_ => {
        // itemData.value = result.data.itemFetchMore
        itemData.value = data.value
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
