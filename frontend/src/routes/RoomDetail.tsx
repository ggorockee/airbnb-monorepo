import {
	Box,
	Grid,
	GridItem,
	Heading,
	Image,
	Skeleton,
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getRoom } from "../api";
import { IRoomDetail } from "../types";

export default function RoomDetail() {
	// useParams 제네릭으로 roomPk가 string임을 명시
	const { roomPk } = useParams<{ roomPk: string }>();

	// useQuery 객체 옵션 형태로, queryFn에는 getRoom(context)를 그대로 넘겨줍니다.
	const { isLoading, data, error } = useQuery<IRoomDetail, Error>({
		queryKey: ["rooms", roomPk],
		queryFn: getRoom,
	});

	if (error) {
		return <p>에러 발생: {error.message}</p>;
	}

	return (
		<Box
			mt={10}
			px={{
				base: 10,
				lg: 40,
			}}
		>
			{/* 방 제목 */}
			<Skeleton height="43px" width="25%" isLoaded={!isLoading}>
				<Heading>{data?.name}</Heading>
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
						<Skeleton isLoaded={!isLoading} h="100%" w="100%">
							<Image
								objectFit="cover"
								w="100%"
								h="100%"
								src={data?.photos[index].file}
							/>
						</Skeleton>
					</GridItem>
				))}
			</Grid>
		</Box>
	);
}
