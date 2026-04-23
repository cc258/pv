import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Table,
  Card,
  PaginationProps,
  Button,
  Space,
  Typography,
  Message,
} from '@arco-design/web-react';
import PermissionWrapper from '@/components/PermissionWrapper';
import { IconDownload, IconPlus } from '@arco-design/web-react/icon';
import request from '@/utils/request';
import useLocale from '@/utils/useLocale';
import SearchForm from './form';
import locale from './locale';
import styles from './style/index.module.less';
import './mock';
import { getColumns } from './constants';


const { Title } = Typography;
export const ContentType = ['图文', '横版短视频', '竖版短视频'];
export const FilterType = ['规则筛选', '人工'];
export const Status = ['已上线', '未上线'];

function SearchTable() {
  const history = useHistory()
  const t = useLocale(locale);


  const actionType = async(r ,type)=>{
    if(type == 'view'){
      history.push(`/list/video-details?id=${r.id}`);
    }else if(type == 'del'){
      request.delete(`/video/${r.id}`).then((res)=>{
        if(res){
          fetchData();
          Message.success(t['searchTable.columns.operations.delete.success']);
        }else{
          Message.error(t['searchTable.columns.operations.delete.failed']);
        }
      })
    }
  }

  const columns = useMemo(() => getColumns(t, actionType), [t]);

  const [data, setData] = useState([]);
  const [pagination, setPatination] = useState<PaginationProps>({
    sizeCanChange: true,
    showTotal: true,
    pageSize: 10,
    current: 1,
    pageSizeChangeResetCurrent: true,
  });
  const [loading, setLoading] = useState(true);
  const [formParams, setFormParams] = useState({});

  useEffect(() => {
    fetchData();
  }, [pagination.current, pagination.pageSize, JSON.stringify(formParams)]);

  function fetchData() {
    const { current, pageSize } = pagination;
    setLoading(true);
    request
      .get('/video', {
        params: {
          page: current,
          size: pageSize,
          ...formParams,
        },
      })
      .then((res) => {
        setData(res.data);
        setPatination({
          ...pagination,
          current,
          pageSize,
          total: res.total,
        });
        setLoading(false);
      });
  }

  function onChangeTable({ current, pageSize }) {
    setPatination({
      ...pagination,
      current,
      pageSize,
    });
  }

  function handleSearch(params) {
    setPatination({ ...pagination, current: 1 });
    setFormParams(params);
  }

  return (
    <Card>
      <Title heading={6}>{t['menu.list.searchTable']}</Title>
      <SearchForm onSearch={handleSearch} />
      <PermissionWrapper
        requiredPermissions={[
          { resource: 'menu.list.searchTable', actions: ['write'] },
        ]}
      >
        <div className={styles['button-group']}>
          <Space>
            <Button onClick={()=>{history.push(`/list/video-details`);}} type="primary" icon={<IconPlus />}>
              {t['searchTable.operations.add']}
            </Button>
            {/* <Button>{t['searchTable.operations.upload']}</Button> */}
          </Space>
          <Space>
            <Button icon={<IconDownload />}>
              {t['searchTable.operation.download']}
            </Button>
          </Space>
        </div>
      </PermissionWrapper>
      <Table
        rowKey="id"
        loading={loading}
        onChange={onChangeTable}
        pagination={pagination}
        columns={columns}
        data={data}
      />
    </Card>
  );
}

export default SearchTable;
