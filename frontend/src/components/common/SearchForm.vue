<template>
  <div class="search-form">
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      :inline="inline"
      :label-width="labelWidth"
      :label-position="labelPosition"
      :size="size"
      :disabled="disabled"
      :validate-on-rule-change="validateOnRuleChange"
      :hide-required-asterisk="hideRequiredAsterisk"
      :show-message="showMessage"
      :inline-message="inlineMessage"
      :status-icon="statusIcon"
      @validate="handleValidate"
      @submit.prevent="handleSubmit"
    >
      <template v-for="field in fields" :key="field.prop">
        <!-- 输入框 -->
        <el-form-item
          v-if="field.type === 'input'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-input
            v-model="formData[field.prop]"
            :type="field.inputType || 'text'"
            :placeholder="field.placeholder"
            :clearable="field.clearable !== false"
            :show-password="field.showPassword"
            :disabled="field.disabled"
            :readonly="field.readonly"
            :maxlength="field.maxlength"
            :minlength="field.minlength"
            :show-word-limit="field.showWordLimit"
            :prefix-icon="field.prefixIcon"
            :suffix-icon="field.suffixIcon"
            :rows="field.rows"
            :autosize="field.autosize"
            :autocomplete="field.autocomplete"
            :name="field.name"
            :max="field.max"
            :min="field.min"
            :step="field.step"
            :resize="field.resize"
            :autofocus="field.autofocus"
            :form="field.form"
            :label="field.inputLabel"
            :tabindex="field.tabindex"
            :validate-event="field.validateEvent"
            @blur="handleFieldBlur(field, $event)"
            @focus="handleFieldFocus(field, $event)"
            @change="handleFieldChange(field, $event)"
            @input="handleFieldInput(field, $event)"
            @clear="handleFieldClear(field)"
          />
        </el-form-item>

        <!-- 选择器 -->
        <el-form-item
          v-else-if="field.type === 'select'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-select
            v-model="formData[field.prop]"
            :placeholder="field.placeholder"
            :clearable="field.clearable !== false"
            :disabled="field.disabled"
            :multiple="field.multiple"
            :multiple-limit="field.multipleLimit"
            :collapse-tags="field.collapseTags"
            :collapse-tags-tooltip="field.collapseTagsTooltip"
            :filterable="field.filterable"
            :allow-create="field.allowCreate"
            :filter-method="field.filterMethod"
            :remote="field.remote"
            :remote-method="field.remoteMethod"
            :loading="field.loading"
            :loading-text="field.loadingText"
            :no-match-text="field.noMatchText"
            :no-data-text="field.noDataText"
            :popper-class="field.popperClass"
            :reserve-keyword="field.reserveKeyword"
            :default-first-option="field.defaultFirstOption"
            :teleported="field.teleported"
            :persistent="field.persistent"
            :automatic-dropdown="field.automaticDropdown"
            :clear-icon="field.clearIcon"
            :fit-input-width="field.fitInputWidth"
            :suffix-icon="field.suffixIcon"
            :tag-type="field.tagType"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
            @visible-change="handleSelectVisibleChange(field, $event)"
            @remove-tag="handleSelectRemoveTag(field, $event)"
            @clear="handleFieldClear(field)"
            @blur="handleFieldBlur(field, $event)"
            @focus="handleFieldFocus(field, $event)"
          >
            <el-option
              v-for="option in field.options"
              :key="option.value"
              :label="option.label"
              :value="option.value"
              :disabled="option.disabled"
            />
          </el-select>
        </el-form-item>

        <!-- 日期选择器 -->
        <el-form-item
          v-else-if="field.type === 'date'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-date-picker
            v-model="formData[field.prop]"
            :type="field.dateType || 'date'"
            :placeholder="field.placeholder"
            :start-placeholder="field.startPlaceholder"
            :end-placeholder="field.endPlaceholder"
            :format="field.format"
            :value-format="field.valueFormat"
            :clearable="field.clearable !== false"
            :disabled="field.disabled"
            :editable="field.editable"
            :readonly="field.readonly"
            :size="field.dateSize"
            :prefix-icon="field.prefixIcon"
            :clear-icon="field.clearIcon"
            :name="field.name"
            :disabled-date="field.disabledDate"
            :shortcuts="field.shortcuts"
            :cell-class-name="field.cellClassName"
            :range-separator="field.rangeSeparator"
            :default-value="field.defaultValue"
            :default-time="field.defaultTime"
            :popper-class="field.popperClass"
            :unlink-panels="field.unlinkPanels"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
            @blur="handleFieldBlur(field, $event)"
            @focus="handleFieldFocus(field, $event)"
            @calendar-change="handleCalendarChange(field, $event)"
            @panel-change="handlePanelChange(field, $event)"
            @visible-change="handleDateVisibleChange(field, $event)"
          />
        </el-form-item>

        <!-- 数字输入框 -->
        <el-form-item
          v-else-if="field.type === 'number'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-input-number
            v-model="formData[field.prop]"
            :min="field.min"
            :max="field.max"
            :step="field.step"
            :step-strictly="field.stepStrictly"
            :precision="field.precision"
            :size="field.numberSize"
            :disabled="field.disabled"
            :controls="field.controls !== false"
            :controls-position="field.controlsPosition"
            :name="field.name"
            :label="field.inputLabel"
            :placeholder="field.placeholder"
            :id="field.id"
            :value-on-clear="field.valueOnClear"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
            @blur="handleFieldBlur(field, $event)"
            @focus="handleFieldFocus(field, $event)"
          />
        </el-form-item>

        <!-- 开关 -->
        <el-form-item
          v-else-if="field.type === 'switch'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-switch
            v-model="formData[field.prop]"
            :disabled="field.disabled"
            :loading="field.loading"
            :size="field.switchSize"
            :width="field.width"
            :inline-prompt="field.inlinePrompt"
            :active-icon="field.activeIcon"
            :inactive-icon="field.inactiveIcon"
            :active-text="field.activeText"
            :inactive-text="field.inactiveText"
            :active-value="field.activeValue"
            :inactive-value="field.inactiveValue"
            :active-color="field.activeColor"
            :inactive-color="field.inactiveColor"
            :border-color="field.borderColor"
            :name="field.name"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
          />
        </el-form-item>

        <!-- 单选框组 -->
        <el-form-item
          v-else-if="field.type === 'radio'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-radio-group
            v-model="formData[field.prop]"
            :size="field.radioSize"
            :disabled="field.disabled"
            :text-color="field.textColor"
            :fill="field.fill"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
          >
            <el-radio
              v-for="option in field.options"
              :key="option.value"
              :label="option.value"
              :disabled="option.disabled"
              :border="field.border"
              :size="field.radioSize"
            >
              {{ option.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 复选框组 -->
        <el-form-item
          v-else-if="field.type === 'checkbox'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <el-checkbox-group
            v-model="formData[field.prop]"
            :size="field.checkboxSize"
            :disabled="field.disabled"
            :min="field.min"
            :max="field.max"
            :text-color="field.textColor"
            :fill="field.fill"
            :tag="field.tag"
            :validate-event="field.validateEvent"
            @change="handleFieldChange(field, $event)"
          >
            <el-checkbox
              v-for="option in field.options"
              :key="option.value"
              :label="option.value"
              :disabled="option.disabled"
              :border="field.border"
              :size="field.checkboxSize"
              :name="option.name"
              :checked="option.checked"
              :true-label="option.trueLabel"
              :false-label="option.falseLabel"
            >
              {{ option.label }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <!-- 自定义插槽 -->
        <el-form-item
          v-else-if="field.type === 'slot'"
          :prop="field.prop"
          :label="field.label"
          :label-width="field.labelWidth"
          :required="field.required"
          :rules="field.rules"
          :error="field.error"
          :show-message="field.showMessage"
          :inline-message="field.inlineMessage"
          :size="field.size"
        >
          <slot :name="field.slot" :field="field" :form-data="formData" />
        </el-form-item>
      </template>

      <!-- 操作按钮 -->
      <el-form-item v-if="showActions" class="form-actions">
        <slot name="actions" :form-data="formData" :reset="handleReset" :submit="handleSubmit">
          <el-button
            v-if="showSearch"
            type="primary"
            :icon="Search"
            :loading="searchLoading"
            @click="handleSubmit"
          >
            {{ searchText }}
          </el-button>
          <el-button
            v-if="showReset"
            :icon="RefreshLeft"
            @click="handleReset"
          >
            {{ resetText }}
          </el-button>
          <el-button
            v-if="showExpand && hasMoreFields"
            type="text"
            :icon="isExpanded ? ArrowUp : ArrowDown"
            @click="toggleExpand"
          >
            {{ isExpanded ? '收起' : '展开' }}
          </el-button>
        </slot>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { Search, RefreshLeft, ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import type { FormRule } from '@/types/global'

// 字段配置接口
interface FormField {
  prop: string
  label: string
  type: 'input' | 'select' | 'date' | 'number' | 'switch' | 'radio' | 'checkbox' | 'slot'
  placeholder?: string
  required?: boolean
  rules?: FormRule[]
  options?: Array<{ label: string; value: any; disabled?: boolean; [key: string]: any }>
  disabled?: boolean
  clearable?: boolean
  labelWidth?: string
  size?: 'large' | 'default' | 'small'
  span?: number
  hidden?: boolean
  slot?: string
  [key: string]: any
}

// 组件属性
interface Props {
  fields: FormField[]
  modelValue?: Record<string, any>
  inline?: boolean
  labelWidth?: string
  labelPosition?: 'left' | 'right' | 'top'
  size?: 'large' | 'default' | 'small'
  disabled?: boolean
  validateOnRuleChange?: boolean
  hideRequiredAsterisk?: boolean
  showMessage?: boolean
  inlineMessage?: boolean
  statusIcon?: boolean
  showActions?: boolean
  showSearch?: boolean
  showReset?: boolean
  showExpand?: boolean
  searchText?: string
  resetText?: string
  searchLoading?: boolean
  expandCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => ({}),
  inline: true,
  labelWidth: '80px',
  labelPosition: 'right',
  size: 'default',
  disabled: false,
  validateOnRuleChange: true,
  hideRequiredAsterisk: false,
  showMessage: true,
  inlineMessage: false,
  statusIcon: false,
  showActions: true,
  showSearch: true,
  showReset: true,
  showExpand: true,
  searchText: '搜索',
  resetText: '重置',
  searchLoading: false,
  expandCount: 3
})

// 事件定义
const emit = defineEmits([
  'update:modelValue',
  'search',
  'reset',
  'field-change',
  'validate'
])

// 响应式数据
const formRef = ref()
const formData = ref<Record<string, any>>({})
const formRules = ref<Record<string, FormRule[]>>({})
const isExpanded = ref(false)

// 计算属性
const hasMoreFields = computed(() => props.fields.length > props.expandCount)

const visibleFields = computed(() => {
  if (!hasMoreFields.value || isExpanded.value) {
    return props.fields
  }
  return props.fields.slice(0, props.expandCount)
})

// 初始化表单数据
const initFormData = () => {
  const data: Record<string, any> = {}
  const rules: Record<string, FormRule[]> = {}
  
  props.fields.forEach(field => {
    // 设置默认值
    if (props.modelValue[field.prop] !== undefined) {
      data[field.prop] = props.modelValue[field.prop]
    } else if (field.type === 'checkbox') {
      data[field.prop] = []
    } else if (field.type === 'switch') {
      data[field.prop] = false
    } else {
      data[field.prop] = ''
    }
    
    // 设置验证规则
    if (field.rules) {
      rules[field.prop] = field.rules
    }
  })
  
  formData.value = data
  formRules.value = rules
}

// 事件处理
const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    emit('search', formData.value)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  emit('reset')
}

const handleValidate = (prop: string, isValid: boolean, message: string) => {
  emit('validate', { prop, isValid, message })
}

const handleFieldChange = (field: FormField, value: any) => {
  formData.value[field.prop] = value
  emit('update:modelValue', formData.value)
  emit('field-change', { field, value, formData: formData.value })
}

const handleFieldBlur = (field: FormField, event: Event) => {
  // 字段失焦事件
}

const handleFieldFocus = (field: FormField, event: Event) => {
  // 字段聚焦事件
}

const handleFieldInput = (field: FormField, value: any) => {
  // 输入事件
}

const handleFieldClear = (field: FormField) => {
  // 清空事件
}

const handleSelectVisibleChange = (field: FormField, visible: boolean) => {
  // 选择器显示/隐藏事件
}

const handleSelectRemoveTag = (field: FormField, tag: any) => {
  // 移除标签事件
}

const handleCalendarChange = (field: FormField, value: any) => {
  // 日历变化事件
}

const handlePanelChange = (field: FormField, value: any) => {
  // 面板变化事件
}

const handleDateVisibleChange = (field: FormField, visible: boolean) => {
  // 日期选择器显示/隐藏事件
}

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

// 公开方法
const validate = () => {
  return formRef.value?.validate()
}

const validateField = (prop: string) => {
  return formRef.value?.validateField(prop)
}

const resetFields = () => {
  formRef.value?.resetFields()
}

const clearValidate = (props?: string | string[]) => {
  formRef.value?.clearValidate(props)
}

const scrollToField = (prop: string) => {
  formRef.value?.scrollToField(prop)
}

// 暴露方法
defineExpose({
  validate,
  validateField,
  resetFields,
  clearValidate,
  scrollToField
})

// 监听器
watch(() => props.modelValue, (newVal) => {
  Object.assign(formData.value, newVal)
}, { deep: true })

watch(() => props.fields, () => {
  initFormData()
}, { immediate: true })

// 初始化
initFormData()
</script>

<style scoped lang="scss">
.search-form {
  .form-actions {
    margin-left: auto;
    
    :deep(.el-form-item__content) {
      display: flex;
      gap: 8px;
    }
  }
}
</style>
