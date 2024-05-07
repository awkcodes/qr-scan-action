import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { getCSRFToken } from './csrf';

export default function OfferRedeem() {
    const { offerId } = useParams();
    const [message, setMessage] = useState('');
    const [confirming, setConfirming] = useState(false);

    useEffect(() => {
        axios.get(`/offers/redeem/${offerId}/`)
            .then(response => setMessage(response.data.message))
            .catch(error => setMessage('Error offer already redeemed'));
    }, [offerId]);

    const handleConfirm = async (confirm) => {
        try {
            const csrfToken = await getCSRFToken();
            const response = await axios.post(
                `/offers/redeem/${offerId}/`,
                { confirm },
                {
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                }
            );
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error redeeming offer');
        }
        setConfirming(false);
    };

    return (
        <div>
            <p>{message}</p>
            {message.includes('Do you want') && (
                <>
                    <button onClick={() => handleConfirm('yes')}>Yes</button>
                    <button onClick={() => handleConfirm('no')}>No</button>
                </>
            )}
        </div>
    );
}
