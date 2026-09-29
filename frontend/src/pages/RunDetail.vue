<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const props = defineProps({ id: String })
const run = ref(null)
const box = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
    try {
      box.value = await getJSON(`/api/boxes/${run.box_id}`)
    } catch {
      box.value = null
    }
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <h1>用纸档 #{{ run.id }}</h1>
      <p class="lede">
        {{ run.box_name || '（盒已删除）' }}
        · {{ run.result?.paper_name || '—' }}
        <span class="pill">写入于 {{ run.created_at }}</span>
      </p>

      <div class="result-board">
        <div class="figure">{{ run.result?.paper_m2 }}<span>m²</span></div>
        <p class="stat-line cut-line">
          卷宽 <strong>{{ run.result?.roll_width }}</strong> m
          → 下料长 <strong>{{ run.result?.sheet_len }}</strong> m
          · 共 <strong>{{ run.result?.sheets }}</strong> 张
        </p>
        <p class="stat-line">
          盒体表面积 {{ run.result?.box_surface }} m² · 折边系数 ×{{ run.result?.overlap }}
          <template v-if="run.result?.wrap_style"> · 丝带样式 {{ run.result.wrap_style }}</template>
        </p>
        <p class="stat-line" v-if="run.result?.ribbon">
          十字丝带约 {{ run.result.ribbon.ribbon_m ?? run.result.ribbon }} m
        </p>
        <p class="stat-line" v-if="run.note">备注：{{ run.note }}</p>
      </div>

      <BoxUnfold
        v-if="box"
        :l="box.length"
        :w="box.width"
        :h="box.height"
        :paper-m2="run.result?.paper_m2"
        :roll-width="run.result?.roll_width"
        :sheet-len="run.result?.sheet_len"
        :sheets="run.result?.sheets"
      />

      <div class="row" style="margin-top: 1.25rem">
        <router-link
          v-if="box"
          class="btn"
          :to="`/bench?box_id=${run.box_id}&paper_id=${run.result?.paper_id}`"
        >同卷同盒再算</router-link>
        <router-link class="btn ghost" to="/history">返回用纸档</router-link>
      </div>
    </template>
  </div>
</template>
