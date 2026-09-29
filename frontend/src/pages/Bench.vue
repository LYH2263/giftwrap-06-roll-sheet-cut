<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const route = useRoute()
const boxes = ref([])
const papers = ref([])
const bid = ref(1)
const pid = ref(null)
const out = ref(null)
const err = ref('')
const busy = ref(false)

onMounted(async () => {
  try {
    const [b, p] = await Promise.all([getJSON('/api/boxes'), getJSON('/api/papers')])
    boxes.value = b.items.filter((x) => x.data_quality === 'clean')
    papers.value = p.items
    const qb = Number(route.query.box_id)
    const qp = Number(route.query.paper_id)
    if (boxes.value.length) bid.value = boxes.value.some((x) => x.id === qb) ? qb : boxes.value[0].id
    const validPapers = papers.value.filter((x) => x.data_quality !== 'dirty' && x.roll_width > 0)
    if (validPapers.length) {
      pid.value = validPapers.some((x) => x.id === qp) ? qp : validPapers[0].id
    }
  } catch (e) {
    err.value = String(e.message || e)
  }
})

async function go(save) {
  err.value = ''
  busy.value = true
  try {
    const q = `box_id=${bid.value}&paper_id=${pid.value}`
    out.value = save
      ? await postJSON('/api/estimate', { box_id: bid.value, paper_id: pid.value, save: true })
      : await getJSON(`/api/estimate?${q}`)
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先选纸卷试算看下料长与张数，确认后再写入用纸档。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <select v-model.number="pid">
        <option v-for="p in papers" :key="p.id" :value="p.id" :disabled="p.data_quality === 'dirty' || p.roll_width <= 0">
          {{ p.name }}（{{ p.roll_width }} m）
        </option>
      </select>
      <button :disabled="busy || pid == null" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy || pid == null" @click="go(true)">写入用纸档</button>
    </div>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="figure">{{ out.paper_m2 }}<span>m²</span></div>
      <p class="stat-line cut-line">
        卷宽 {{ out.roll_width }} m → 下料长 <strong>{{ out.sheet_len }}</strong> m · 共 <strong>{{ out.sheets }}</strong> 张
      </p>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m
      </p>
      <BoxUnfold
        :l="out.box.length"
        :w="out.box.width"
        :h="out.box.height"
        :paper-m2="out.paper_m2"
        :roll-width="out.roll_width"
        :sheet-len="out.sheet_len"
        :sheets="out.sheets"
      />
    </div>
  </div>
</template>
