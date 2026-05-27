<script setup>
import { ref, computed } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import TextAlign from '@tiptap/extension-text-align'
import { api } from '../services/api.js'

const props = defineProps({ peticao: Object })

const expandido = ref(false)
const salvando = ref(false)
const status = ref(props.peticao.status)  // gerada | aprovada | rejeitada | erro

const editor = useEditor({
  content: props.peticao.conteudo || '',
  extensions: [
    StarterKit,
    TextAlign.configure({ types: ['paragraph'] }),
  ],
  editorProps: {
    attributes: {
      class: 'prose prose-sm max-w-none p-4 min-h-48 focus:outline-none font-serif text-sm leading-relaxed'
    }
  }
})

const conteudoAtual = computed(() => editor.value?.getText() || props.peticao.conteudo)

async function baixarDocx() {
  salvando.value = true
  try {
    await api.baixarDocx(props.peticao.numero, conteudoAtual.value)
    status.value = 'aprovada'
  } finally {
    salvando.value = false
  }
}

async function baixarPdf() {
  salvando.value = true
  try {
    await api.baixarPdf(props.peticao.numero, conteudoAtual.value)
    status.value = 'aprovada'
  } finally {
    salvando.value = false
  }
}

const corStatus = {
  gerada:    'bg-yellow-100 text-yellow-700',
  aprovada:  'bg-green-100 text-green-700',
  rejeitada: 'bg-red-100 text-red-700',
  erro:      'bg-red-100 text-red-700',
}
</script>

<template>
  <div class="card">
    <!-- Cabeçalho do card -->
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-1">
          <span
            class="text-xs font-medium px-2 py-0.5 rounded-full"
            :class="corStatus[status] || 'bg-gray-100 text-gray-600'"
          >
            {{ status }}
          </span>
          <span class="text-xs text-gray-400">{{ peticao.modelo_usado }}</span>
        </div>
        <h3 class="font-mono text-blue-700 font-bold">{{ peticao.numero }}</h3>
      </div>

      <!-- Ações -->
      <div class="flex gap-2 ml-4">
        <template v-if="status !== 'erro'">
          <button
            class="btn-success text-xs py-1.5 px-3"
            :disabled="salvando"
            @click="baixarDocx"
          >
            📄 Word
          </button>
          <button
            class="btn-primary text-xs py-1.5 px-3"
            :disabled="salvando"
            @click="baixarPdf"
          >
            📕 PDF
          </button>
        </template>
        <button
          class="btn-secondary text-xs py-1.5 px-3"
          @click="expandido = !expandido"
        >
          {{ expandido ? '▲ Fechar' : '▼ Editar' }}
        </button>
        <button
          v-if="status !== 'rejeitada'"
          class="btn-danger text-xs py-1.5 px-3"
          @click="status = 'rejeitada'"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Erro -->
    <p v-if="status === 'erro'" class="mt-3 text-red-600 text-sm">
      ❌ {{ peticao.erro }}
    </p>

    <!-- Editor expansível -->
    <div v-if="expandido && status !== 'erro'" class="mt-4">
      <div class="border border-gray-200 rounded-lg overflow-hidden">
        <!-- Toolbar mínima -->
        <div class="bg-gray-50 border-b border-gray-200 px-3 py-1.5 flex gap-2 text-xs">
          <button
            class="px-2 py-1 rounded hover:bg-gray-200"
            :class="editor?.isActive('bold') ? 'bg-gray-200 font-bold' : ''"
            @click="editor?.chain().focus().toggleBold().run()"
          >B</button>
          <button
            class="px-2 py-1 rounded hover:bg-gray-200 italic"
            @click="editor?.chain().focus().toggleItalic().run()"
          >I</button>
          <span class="w-px bg-gray-300 mx-1"></span>
          <button
            class="px-2 py-1 rounded hover:bg-gray-200"
            @click="editor?.chain().focus().setTextAlign('left').run()"
          >⬅</button>
          <button
            class="px-2 py-1 rounded hover:bg-gray-200"
            @click="editor?.chain().focus().setTextAlign('justify').run()"
          >☰</button>
        </div>
        <!-- Área de edição -->
        <EditorContent :editor="editor" />
      </div>
      <p class="text-xs text-gray-400 mt-1">✏️ Edite o texto acima antes de exportar.</p>
    </div>
  </div>
</template>
