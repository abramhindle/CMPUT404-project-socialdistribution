import React from 'react';

import { Layout, Menu, Breadcrumb } from 'antd';

const { Header, Content, Footer } = Layout;
const CustomLayout = (props) => {
    return (
        <Layout>
            <Header>Header</Header>
            <Content>
                {props.children}
            </Content>
            <Footer styles={{textAlign:'center'}}>Created By Team 5</Footer>
        </Layout>
    );
}

export default CustomLayout;
