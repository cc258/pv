import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { Card, Tree, Switch, Typography, Alert, Spin, Space, Tag } from '@arco-design/web-react';
import request from '@/utils/request';
import useLocale from '@/utils/useLocale';
import locale from './locale';
import styles from './style/index.module.less';

const { Title, Text } = Typography;

interface Permission {
  id: number;
  code: string;
  description: string;
}

interface Role {
  id: number;
  name: string;
  description: string;
  permissions: Permission[];
}

interface RolePermissionData {
  roles: Role[];
  permissions: Permission[];
}

interface TreeNode {
  key: string;
  title: React.ReactNode;
  children?: TreeNode[];
  isLeaf?: boolean;
}

function PermissionManagement() {
  const t = useLocale(locale);
  const userInfo = useSelector((state: any) => state.userInfo);
  const userLoading = useSelector((state: any) => state.userLoading);
  
  const [data, setData] = useState<RolePermissionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const res: RolePermissionData = await request.get('/roles/permissions');
      setData(res);
      if (res?.roles?.length > 0 && !selectedRoleId) {
        setSelectedRoleId(res.roles[0].id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取权限数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePermissionToggle = async (roleId: number, permissionId: number, checked: boolean) => {
    try {
      await request.post(`/roles/${roleId}/permissions/${permissionId}?action=${checked ? 'add' : 'remove'}`);
      
      await fetchData();
    } catch (err: any) {
      setError(err.response?.data?.detail || '操作失败');
    }
  };

  const buildTreeData = (roles: Role[], permissions: Permission[]): TreeNode[] => {
    const resourceMap: Record<string, { label: string, permissions: Permission[] }> = {};
    
    permissions.forEach(perm => {
      const [resource] = perm.code.split(':');
      if (!resourceMap[resource]) {
        resourceMap[resource] = { label: resource, permissions: [] };
      }
      resourceMap[resource].permissions.push(perm);
    });

    const resourceLabels: Record<string, string> = {
      user: '用户管理',
      video: '视频管理',
      role: '角色管理',
      permission: '权限管理',
      menu: '菜单管理',
    };

    return Object.entries(resourceMap).map(([resource, group]) => ({
      key: `resource_${resource}`,
      title: resourceLabels[resource] || resource,
      children: group.permissions.map(perm => ({
        key: `perm_${perm.id}`,
        isLeaf: true,
        title: (
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Text>{perm.description}</Text>
            <Space>
              {roles.map(role => {
                const hasPermission = role.permissions.some(p => p.id === perm.id);
                return (
                  <Space key={role.id} size={4}>
                    <Tag size="small" color="arcoblue">{role.name}</Tag>
                    <Switch
                      checked={hasPermission}
                      onChange={(checked) => handlePermissionToggle(role.id, perm.id, checked)}
                      size="small"
                    />
                  </Space>
                );
              })}
            </Space>
          </Space>
        ),
      })),
    }));
  };

  if (userLoading || !data) {
    return <Spin />;
  }

  const treeData = buildTreeData(data.roles, data.permissions);

  return (
    <div className={styles.container}>
      <Card>
        <Title heading={5}>{t['permissionManagement.title']}</Title>
        <Text type="secondary">{t['permissionManagement.description']}</Text>
        
        {error && (
          <Alert type="error" content={error} style={{ marginTop: 16 }} />
        )}
        
        <div style={{ marginTop: 16 }}>
          <Tree
            treeData={treeData}
            showLine
            blockNode
          />
        </div>
      </Card>
    </div>
  );
}

export default PermissionManagement;
