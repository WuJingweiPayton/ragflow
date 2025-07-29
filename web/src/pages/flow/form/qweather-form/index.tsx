import { useTranslate } from '@/hooks/common-hooks';
import { Form, Input, Select } from 'antd';
import { useCallback, useMemo } from 'react';
import { IOperatorForm } from '../../interface';
import DynamicInputVariable from '../components/dynamic-input-variable';

const QWeatherForm = ({ onValuesChange, form, node }: IOperatorForm) => {
  const { t } = useTranslate('flow');
  // 删除 QWeather 相关选项的 import 和相关使用

  const getQWeatherTimePeriodOptions = useCallback(
    (userType: string) => {
      let options = QWeatherTimePeriodOptions;
      if (userType === 'free') {
        options = options.slice(0, 3);
      }
      return options.map((x) => ({
        value: x,
        label: t(`qWeatherTimePeriodOptions.${x}`),
      }));
    },
    [t],
  );

  return (
    <Form
      name="basic"
      autoComplete="off"
      form={form}
      onValuesChange={onValuesChange}
      layout={'vertical'}
    >
      <DynamicInputVariable node={node}></DynamicInputVariable>
      <Form.Item label={t('webApiKey')} name={'web_apikey'}>
        <Input></Input>
      </Form.Item>
      <Form.Item label={t('lang')} name={'lang'}>
        <Select options={qWeatherLangOptions}></Select>
      </Form.Item>
      <Form.Item label={t('type')} name={'type'}>
        <Select options={qWeatherTypeOptions}></Select>
      </Form.Item>
      <Form.Item label={t('userType')} name={'user_type'}>
        <Select options={qWeatherUserTypeOptions}></Select>
      </Form.Item>
      <Form.Item noStyle dependencies={['type', 'user_type']}>
        {({ getFieldValue }) =>
          getFieldValue('type') === 'weather' && (
            <Form.Item label={t('timePeriod')} name={'time_period'}>
              <Select
                options={getQWeatherTimePeriodOptions(
                  getFieldValue('user_type'),
                )}
              ></Select>
            </Form.Item>
          )
        }
      </Form.Item>
    </Form>
  );
};

export default QWeatherForm;
