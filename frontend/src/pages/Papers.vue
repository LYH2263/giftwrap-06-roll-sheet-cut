<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const items = ref([])
const err = ref('')
const saving = ref(null)

async function load() {
  err.value = ''
  try {
    items.value = (await getJSON('/api/papers')).items
  } catch (e) {
    err.value = String(e.message || e)
  }
}

async function save(p) {
  err.value = ''
  saving.value = p.id
  try {
    await putJSON(`/api/papers/${p.id}`, { name: p.name, roll_width: Number(p.roll_width) })
    await load()
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    saving.value = null
  }
}

onMounted(load)
</script>

<template>
  <div class="page">
    <h1>包装纸</h1>
    <p class="lede">卷宽用于下料裁切：下料长 = 用纸面积 ÷ 卷宽，张数按单张 1m 向上取整。改卷宽只影响之后的新单，已写入用纸档的卷宽与张数钉住不变。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-else class="paper-grid">
      <div v-for="p in items" :key="p.id" class="paper-tile">
        <strong>{{ p.name }}</strong>
        <label class="meta">
          卷宽
          <input
            v-model.number="p.roll_width"
            type="number"
            step="0.05"
            min="0.1"
            class="roll-input"
            :disabled="saving === p.id"
          />
          m
        </label>
        <button class="btn ghost" :disabled="saving === p.id || p.roll_width <= 0" @click="save(p)">
          {{ saving === p.id ? '保存中…' : '保存卷宽' }}
        </button>
      </div>
    </div>
  </div>
</template>
