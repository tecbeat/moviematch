import React, { useState, useEffect } from 'react';
import '../Section/Section.css'
import './Matching.css'
import Loading from '../Loading/Loading'
import RateButton from '../Button/RateButton'
import { MovieThumbnail } from '../Image/MovieThumbnail'
import { likeButton, neutralButton, dislikeButton } from './Data';
import { AiFillStar } from 'react-icons/ai';
import APIHandler from '../../manage/api/APIHandler';


function Matching({
    kind,
    dataPath,
    endpoint,
    BASE_THUMBNAIL_URL,
    IMAGE_HEIGHT,
    MAX_DESC_LENGTH,
    emptyImage
}) {
    
    const [state, setState] = useState({
        loaded: false,
        thumbnailSrc: '',
        title: '',
        desc: '',
        runtime: 0,
        rating: 0,
        genres: 'none'
    });

    const [like, setLike] = useState('');
    useEffect(() => {
        getMovie();
    }, []);


    const getMovie = (info) => {
        setLike(info);
        setState({
            loaded: false,
            thumbnailSrc: '',
            title: '',
            desc: '',
            runtime: 0,
            rating: 0,
            genres: 'none'
        });
     
        APIHandler.getRequest(endpoint, {
                "user_id": localStorage.getItem("uid"),
                "usage": kind,
                "path": dataPath
            }).then(data => {
            setState({
                loaded: true,
                thumbnailSrc: (data.thumbnailSrc == null)
                    ? emptyImage
                    : BASE_THUMBNAIL_URL + data.thumbnailSrc,
                title: data.titel,
                desc: (data.desc.length > MAX_DESC_LENGTH)
                    ? data.desc.substring(0, MAX_DESC_LENGTH - 3) + '...'
                    : data.desc,
                runtime: data.runtime,
                rating: data.rating,
                genres: data.genres
            });
        }).catch(err => {
            setState({
                loaded: false,
                thumbnailSrc: '',
                title: '',
                desc: '',
                runtime: 0,
                rating: 0,
                genres: 'none'
            });
            setTimeout(() => getMovie(), 3000);
        });
    };

    return (
        <>
            <div className='darkBg'>

                <nav className='movieThumbnailDesktop'>

                    <div className='movieThumbnailRow'>
                        {state.loaded ? "" : <Loading />}
                        <MovieThumbnail
                            src={state.thumbnailSrc}
                            height={IMAGE_HEIGHT}
                        />
                        <div>
                            <h2 className='movieTitle'>{state.title}</h2>
                            <p className='home__sek-subtitle movieDescription'>{state.desc}</p>
                        </div>
                    </div>
                    <div align='center'>
                        <RateButton {...likeButton} onClick={() => getMovie('like')} />
                        <RateButton {...neutralButton} onClick={() => getMovie('neutral')} />
                        <RateButton {...dislikeButton} onClick={() => getMovie('dislike')} />
                    </div>
                </nav>
                <nav className='movieThumbnailMobile'>
                    <div>
                        <div className='movieThumbnailRow'>
                            {state.loaded ? "" : <Loading />}
                            <MovieThumbnail src={state.thumbnailSrc} height={IMAGE_HEIGHT} />
                            <div align='center'>
                                <RateButton {...likeButton} onClick={() => getMovie('like')} />
                                <RateButton {...neutralButton} onClick={() => getMovie('neutral')} />
                                <RateButton {...dislikeButton} onClick={() => getMovie('dislike')} />
                            </div>
                            <div>
                                <h2 className='movieTitle'>{state.title}</h2>
                                <p className='home__sek-subtitle movieDescription'>{state.desc}</p>
                            </div>
                        </div>
                    </div>
                </nav>
            </div>
            <div className="movieInfo">
                <table className="movieTable">
                    <tr>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Runtime</p>
                                <p className='movieInfoText'>{state.runtime} minutes</p>
                            </div>
                        </td>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Rating</p>
                                <p className='movieInfoText'><AiFillStar /> {state.rating}</p>
                            </div>
                        </td>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Genres</p>
                                <p className='movieInfoText'>{state.genres}</p>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </>
    );
}

export default Matching;