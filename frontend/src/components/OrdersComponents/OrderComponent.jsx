import React from 'react';

const OrderComponent = ({order}) => {
    return (
        <tr>
            <td>{order.id}</td>
            <td>{order.name || 'null'}</td>
            <td>{order.surname || 'null'}</td>
            <td>{order.email || 'null'}</td>
            <td>{order.phone || 'null'}</td>
            <td>{order.age ?? 'null'}</td>
            <td>{order.course || 'null'}</td>
            <td>{order.course_format || 'null'}</td>
            <td>{order.course_type || 'null'}</td>
            <td>{order.status || 'null'}</td>
            <td>{order.sum ?? 'null'}</td>
            <td>{order.alreadyPaid ?? 'null'}</td>
            <td>{order.created_at || 'null'}</td>
        </tr>
    );
};

export default OrderComponent;