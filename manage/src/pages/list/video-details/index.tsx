import React, { useState, useRef } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import {
  Typography,
  Card,
  Form,
  Select,
  Input,
  Grid,
  Space,
  Button,
  Message,
} from '@arco-design/web-react';
import { FormInstance } from '@arco-design/web-react/es/Form';
import axios from 'axios';
import useLocale from '@/utils/useLocale';
import locale from './locale';
import styles from './style/index.module.less';
import './mock';

function GroupForm() {
  const t = useLocale(locale);
  const formRef = useRef<FormInstance>();
  const [loading, setLoading] = useState(false);
  
  // v5 获取状态数据
  const location = useLocation();
  const initialValues = location.state || {};
  console.log('initialValues: ',initialValues)

  function submit(data) {
    setLoading(true);
    axios
      .put(`/api/video/${location.state.id}`, {
        data,
      })
      .then(() => {
        Message.success(t['groupForm.submitSuccess']);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  function handleSubmit() {
    formRef.current.validate().then((values) => {
      submit(values);
    });
  }

  function handleReset() {
    formRef.current.resetFields();
  }

  return (
    <div className={styles.container}>
      <Form layout="vertical" ref={formRef} className={styles['form-group']} initialValues={initialValues}>
        <Card>
          <Typography.Title heading={6}>
            {t['groupForm.title.video.info']}
          </Typography.Title>
          <Grid.Row gutter={80}>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.name']}
                field="video_name"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.stars']}
                field="stars"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.year']}
                field="year"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
          </Grid.Row>
          {/* Row 2 */}
          <Grid.Row gutter={80}>
          <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.tags']}
                field="tags"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.categories']}
                field="categories"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.cover']}
                field="cover"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
          </Grid.Row>
          {/* Row 3 */}
          <Grid.Row gutter={80}>
            <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.link']}
                field="link"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
            <Form.Item
                label={t['groupForm.form.label.video.comment']}
                field="comment"
              >
                <Input />
              </Form.Item>
            </Grid.Col>
          </Grid.Row>
        </Card>
      </Form>
      <div className={styles.actions}>
        <Space>
          <Button onClick={handleReset} size="large">
            {t['groupForm.reset']}
          </Button>
          <Button
            type="primary"
            onClick={handleSubmit}
            loading={loading}
            size="large"
          >
            {t['groupForm.submit']}
          </Button>
        </Space>
      </div>
    </div>
  );
}

export default GroupForm;
