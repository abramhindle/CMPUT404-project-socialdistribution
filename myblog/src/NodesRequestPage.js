import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import NodesRequestContent from './components/NodesRequestContent';

function AuthorPage() {
  return (
    <div>
      <Layout>
        <AdminHeader></AdminHeader>
        <Layout>
            <AdminSideBar defaultSelectedKeys="NodesRequest"></AdminSideBar>
            <Layout style={{ padding: '12px 24px 24px'}}><NodesRequestContent/></Layout>
        </Layout>
    </Layout>
    </div>
  );
}

export default AuthorPage;