import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Typography,
  Card,
  Form,
  Select,
  Input,
  InputNumber,
  Grid,
  Space,
  Button,
  Message,
  Tag,
  Rate,
} from '@arco-design/web-react';
import { OptionInfo } from '@arco-design/web-react/es/Select/interface';
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
  const [categories, setCategories] = useState<
    Array<{ id: number; name: string; description?: string }>
  >([]);
  const [categoriesLoading, setCategoriesLoading] = useState(false);
  const [categoriesLoaded, setCategoriesLoaded] = useState(false);

  const location = useLocation();
  const { id } = qs.parse(location.search);
  const videoId = Array.isArray(id) ? id[0] : id;

  function loadCategories() {
    if (categoriesLoaded) return Promise.resolve();
    setCategoriesLoading(true);
    return request
      .get('/categories')
      .then((list) => {
        const data = Array.isArray(list)
          ? (list as Array<{ id: number; name: string; description?: string }>)
          : [];
        setCategories(data);
        setCategoriesLoaded(true);
        return data;
      })
      .catch((err) => {
        Message.error(
          err?.response?.data?.detail ||
            err?.message ||
            t['groupForm.message.loadCategoriesFailed'] ||
            '分类加载失败'
        );
        return [] as Array<{ id: number; name: string; description?: string }>;
      })
      .finally(() => setCategoriesLoading(false));
  }

  function submit(data: Record<string, unknown>) {
    setLoading(true);
    const quest = videoId
      ? request.put(`/video/${videoId}`, data)
      : request.post(`/video`, data);
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
      const categoryIds = Array.isArray(values.categories)
        ? (values.categories as unknown[]).map((c) =>
            typeof c === 'object' && c && 'id' in c ? Number((c as { id: unknown }).id) : Number(c)
          ).filter((n) => Number.isFinite(n))
        : [];

      const submitData = {
        video_name: values.video_name || null,
        link: values.link || null,
        year: typeof values.year === 'number' ? values.year : null,
        cover: values.cover || null,
        tags: values.tags || null,
        category_ids: categoryIds,
        comment: values.comment || null,
        stars: typeof values.stars === 'number' ? values.stars : 1,
      };
      submit(submitData);
    });
  }

  function handleReset() {
    if (videoId) {
      getVideo();
    } else {
      formRef.current.resetFields();
    }
  }

  const getVideo = () => {
    if (videoId) {
      request.get(`/video/${videoId}`).then((res) => {
        const data = (res ?? {}) as {
          id?: string;
          video_name?: string;
          link?: string | null;
          year?: number | null;
          cover?: string | null;
          tags?: string | null;
          comment?: string | null;
          stars?: number;
          categories?: Array<{ id: number; name: string; description?: string }>;
        };
        if (formRef.current) {
          const categoriesField = (data.categories ?? []).map((c) => c.id);
          formRef.current.setFieldsValue({
            ...data,
            categories: categoriesField,
          });
        }
      });
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    getVideo();
  }, [videoId]);

  const categoryOptions = categories.map((c) => ({
    value: c.id,
    label: c.name,
  }));

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
                <Input
                  placeholder={
                    t['groupForm.placeholder.video.name'] || '请输入视频标题'
                  }
                  allowClear
                />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.stars']}
                field="stars"
                rules={[
                  {
                    validator: (value, callback) => {
                      if (value === undefined || value === null || value === '') {
                        callback?.();
                        return;
                      }
                      const n = Number(value);
                      if (n >= 1 && n <= 5) {
                        callback?.();
                      } else {
                        callback?.(
                          t['groupForm.validation.starsRange'] || '星级范围为 1~5'
                        );
                      }
                    },
                  },
                ]}
              >
                <Rate count={5} allowHalf={false} />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.year']}
                field="year"
                rules={[
                  {
                    validator: (value, callback) => {
                      if (value === undefined || value === null || value === '') {
                        callback?.();
                        return;
                      }
                      const n = Number(value);
                      const now = new Date().getFullYear();
                      if (Number.isFinite(n) && n >= 1888 && n <= now + 5) {
                        callback?.();
                      } else {
                        callback?.(
                          t['groupForm.validation.yearRange'] ||
                            `请输入 1888 ~ ${now + 5} 之间的年份`
                        );
                      }
                    },
                  },
                ]}
              >
                <InputNumber
                  min={1888}
                  max={new Date().getFullYear() + 5}
                  step={1}
                  style={{ width: '100%' }}
                  placeholder={t['groupForm.placeholder.video.year'] || '请输入年份'}
                />
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
                <Input
                  placeholder={
                    t['groupForm.placeholder.video.tags'] ||
                    '多个标签可用逗号分隔，如：科幻,动作'
                  }
                  allowClear
                />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.categories']}
                field="categories"
              >
                <Select
                  mode="multiple"
                  loading={categoriesLoading}
                  placeholder={
                    t['groupForm.placeholder.video.categories'] ||
                    '请选择分类（可多选）'
                  }
                  options={categoryOptions}
                  allowClear
                  renderFormat={(option: OptionInfo | null) => {
                    if (!option) return null;
                    const labelText =
                      typeof option.children === 'string'
                        ? option.children
                        : String(option.value ?? '');
                    return <Tag color="arcoblue">{labelText}</Tag>;
                  }}
                />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.cover']}
                field="cover"
              >
                <Input
                  placeholder={
                    t['groupForm.placeholder.video.cover'] || '请输入封面图片链接'
                  }
                  allowClear
                />
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
                <Input
                  placeholder={
                    t['groupForm.placeholder.video.link'] || '请输入视频链接'
                  }
                  allowClear
                />
              </Form.Item>
            </Grid.Col>
            <Grid.Col span={8}>
              <Form.Item
                label={t['groupForm.form.label.video.comment']}
                field="comment"
              >
                <Input.TextArea
                  placeholder={
                    t['groupForm.placeholder.video.comment'] || '请输入备注信息'
                  }
                  autoSize={{ minRows: 2, maxRows: 6 }}
                  maxLength={2000}
                  showWordLimit
                />
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
