import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
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
import request from '@/utils/request';
import qs from 'query-string';
import useLocale from '@/utils/useLocale';
import locale from './locale';
import styles from './style/index.module.less';
import './mock';

function GroupForm() {
  const t = useLocale(locale);
  const formRef = useRef<FormInstance>(null);
  const [loading, setLoading] = useState(false);
  
  const location = useLocation();
  const { id } = qs.parse(location.search);
  console.log(id);

  function submit(data) {
    setLoading(true);
    const quest = id ? request.put(`/video/${id}`, data) : request.post(`/video`, data)
    quest
      .then(() => {
        Message.success(t['groupForm.submitSuccess']);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  function handleSubmit() {
    formRef.current.validate().then((values) => {
      const submitData = {
        video_name: values.video_name || null,
        link: values.link || null,
        year: values.year || null,
        cover: values.cover || null,
        tags: values.tags || null,
        categories: values.categories || null,
        comment: values.comment || null,
        stars: values.stars || 1, // 星级默认1
      };
      submit(submitData);
    });
  }

  function handleReset() {
    if(id){
      getVideo();
    }else{
      formRef.current.resetFields();
    }
  }

  const getVideo = () =>{
    if(id){
      request.get(`/video/${id}`).then((res)=>{
        if(res && formRef.current){
          const data = res;
          formRef.current.setFieldsValue(data);
        }
      })
    }
  }

  useEffect(() => {
    getVideo();
  }, [id]);

  return (
    <div className={styles.container}>
      <Form layout="vertical" ref={formRef} className={styles['form-group']}>
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
