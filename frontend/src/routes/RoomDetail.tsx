import {
	Avatar,
	Box,
	Grid,
	GridItem,
	Heading,
	HStack,
	Image,
	Skeleton,
	Text,
	VStack,
} from "@chakra-ui/react";
import { FaStar } from "react-icons/fa";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getRoom, getRoomReviews } from "../api";
import { IReview, IRoomDetail } from "../types";

export default function RoomDetail() {
	// 1) roomPk가 string임을 명시
	const { roomPk } = useParams<{ roomPk: string }>();

	// 2) useQuery 객체옵션 형태 + 제네릭 지정
	const {
		isLoading: isRoomLoading,
		data: roomData,
		error: roomError,
	} = useQuery<IRoomDetail, Error>({
		queryKey: ["rooms", roomPk],
		queryFn: getRoom,
	});

	const {
		isLoading: isReviewsLoading,
		data: reviewsData = [],
		error: reviewsError,
	} = useQuery<IReview[], Error>({
		queryKey: ["rooms", roomPk, "reviews"],
		queryFn: getRoomReviews,
	});

	// 3) 에러 핸들링
	if (roomError) {
		return <p>방 정보 로딩 중 에러: {roomError.message}</p>;
	}
	if (reviewsError) {
		return <p>리뷰 로딩 중 에러: {reviewsError.message}</p>;
	}

	const isLoading = isRoomLoading || isReviewsLoading;

	return (
		<Box
			pb={40}
			mt={10}
			px={{
				base: 10,
				lg: 40,
			}}
		>
			{/* 방 제목 */}
			<Skeleton height="43px" width="25%" isLoaded={!isRoomLoading}>
				<Heading>{roomData?.name}</Heading>
			</Skeleton>

			{/* 사진 그리드 */}
			<Grid
				mt={8}
				rounded="xl"
				overflow="hidden"
				gap={2}
				height="60vh"
				templateRows="1fr 1fr"
				templateColumns="repeat(4, 1fr)"
			>
				{[0, 1, 2, 3, 4].map((index) => (
					<GridItem
						key={index}
						colSpan={index === 0 ? 2 : 1}
						rowSpan={index === 0 ? 2 : 1}
						overflow="hidden"
					>
						<Skeleton isLoaded={!isRoomLoading} h="100%" w="100%">
							<Image
								objectFit="cover"
								w="100%"
								h="100%"
								src={roomData?.photos[index]?.file}
							/>
						</Skeleton>
					</GridItem>
				))}
			</Grid>

			{/* 호스트 정보 */}
			<HStack width="40%" justifyContent="space-between" mt={10}>
				<VStack alignItems="flex-start">
					<Skeleton isLoaded={!isRoomLoading} height="30px">
						<Heading fontSize="2xl">
							House hosted by {roomData?.owner.name}
						</Heading>
					</Skeleton>
					<Skeleton isLoaded={!isRoomLoading} height="30px">
						<HStack justifyContent="flex-start" w="100%">
							<Text>
								{roomData?.toilets} toilet
								{roomData?.toilets === 1 ? "" : "s"}
							</Text>
							<Text>∙</Text>
							<Text>
								{roomData?.rooms} room
								{roomData?.rooms === 1 ? "" : "s"}
							</Text>
						</HStack>
					</Skeleton>
				</VStack>
				<Avatar
					name={roomData?.owner.name}
					size="xl"
					src={roomData?.owner.avatar}
				/>
			</HStack>

			{/* 평점 & 리뷰 개수 */}
			<Box mt={10}>
				<Heading fontSize="2xl">
					<HStack>
						<FaStar /> <Text>{roomData?.rating}</Text>
						<Text>∙</Text>
						<Text>
							{reviewsData.length} review
							{reviewsData.length === 1 ? "" : "s"}
						</Text>
					</HStack>
				</Heading>
			</Box>
		</Box>
	);
}
