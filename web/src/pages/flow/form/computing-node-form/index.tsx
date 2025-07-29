import LLMSelect from '@/components/llm-select';
import MessageHistoryWindowSizeItem from '@/components/message-history-window-size-item';
import TopNItem from '@/components/top-n-item';
import { useTranslate } from '@/hooks/common-hooks';
import { Form, InputNumber, Switch } from 'antd';
import { IOperatorForm } from '../../interface';
import DynamicInputVariable from '../components/dynamic-input-variable';

const ComputingNodeForm = ({ onValuesChange, form, node }: IOperatorForm) => {
  const { t } = useTranslate('flow');

  return (
    <Form
      name="basic"
      autoComplete="off"
      form={form}
      onValuesChange={onValuesChange}
      layout={'vertical'}
    >
      <DynamicInputVariable node={node}></DynamicInputVariable>
      <TopNItem initialValue={8} max={99}></TopNItem>
      <Form.Item
        name={'similarity_threshold'}
        label={t('similarityThreshold')}
        tooltip={t('similarityThresholdTip')}
        initialValue={0.2}
      >
        <InputNumber
          min={0}
          max={1}
          step={0.1}
          style={{ width: '100%' }}
        />
      </Form.Item>
      <Form.Item
        name={'keywords_similarity_weight'}
        label={t('keywordsSimilarityWeight')}
        tooltip={t('keywordsSimilarityWeightTip')}
        initialValue={0.3}
      >
        <InputNumber
          min={0}
          max={1}
          step={0.1}
          style={{ width: '100%' }}
        />
      </Form.Item>
      <Form.Item
        name={'use_kg'}
        label={t('useKg')}
        tooltip={t('useKgTip')}
        initialValue={false}
        valuePropName="checked"
      >
        <Switch />
      </Form.Item>
      <MessageHistoryWindowSizeItem
        initialValue={12}
      ></MessageHistoryWindowSizeItem>
    </Form>
  );
};

export default ComputingNodeForm; 